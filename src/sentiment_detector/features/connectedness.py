"""
Entropy-Based Connectedness Measures for Sentiment Networks.

This module implements connectedness measures based on Granger causality
and Transfer Entropy networks, following Cao et al. (2025).

Key features:
- Total Connectedness Index (TCI)
- Directional spillovers (TO/FROM)
- Net spillover positions
- Dynamic connectedness over rolling windows
- Centrality measures for identifying key sentiment transmitters
"""

from dataclasses import dataclass, field
from typing import Optional, Union
import logging

import numpy as np
import pandas as pd
from scipy import linalg

from .granger_causality import CausalityNetwork, GrangerCausalityAnalyzer
from .transfer_entropy import InformationFlowNetwork, TransferEntropyAnalyzer

logger = logging.getLogger(__name__)


@dataclass
class ConnectednessResult:
    """
    Result of connectedness analysis.
    
    Attributes:
        total_connectedness: Total Connectedness Index (0-100%)
        to_spillovers: Spillover TO each node from others
        from_spillovers: Spillover FROM each node to others
        net_spillovers: Net spillover position (TO - FROM)
        pairwise_spillovers: NxN matrix of pairwise spillovers
        node_names: Names of nodes
        metadata: Analysis metadata
    """
    total_connectedness: float
    to_spillovers: dict[str, float]
    from_spillovers: dict[str, float]
    net_spillovers: dict[str, float]
    pairwise_spillovers: np.ndarray
    node_names: list[str]
    metadata: dict = field(default_factory=dict)
    
    def get_transmitters(self) -> list[str]:
        """Get nodes that are net transmitters (positive net spillover)."""
        return [k for k, v in self.net_spillovers.items() if v > 0]
    
    def get_receivers(self) -> list[str]:
        """Get nodes that are net receivers (negative net spillover)."""
        return [k for k, v in self.net_spillovers.items() if v < 0]
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert to DataFrame with spillover table."""
        n = len(self.node_names)
        
        # Build spillover table
        data = []
        for i, source in enumerate(self.node_names):
            row = {target: self.pairwise_spillovers[i, j] 
                   for j, target in enumerate(self.node_names)}
            row["FROM_others"] = self.from_spillovers[source]
            data.append(row)
        
        df = pd.DataFrame(data, index=self.node_names)
        
        # Add TO row
        to_row = {target: self.to_spillovers[target] for target in self.node_names}
        to_row["FROM_others"] = self.total_connectedness
        df.loc["TO_others"] = to_row
        
        return df


@dataclass
class DynamicConnectedness:
    """
    Dynamic connectedness over time.
    
    Attributes:
        dates: Timestamps for each window
        total_connectedness: TCI over time
        net_spillovers: Net spillovers over time for each node
        window_size: Rolling window size used
    """
    dates: list
    total_connectedness: list[float]
    net_spillovers: dict[str, list[float]]
    window_size: int
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert to DataFrame."""
        data = {"total_connectedness": self.total_connectedness}
        data.update({f"net_{k}": v for k, v in self.net_spillovers.items()})
        return pd.DataFrame(data, index=self.dates)


class ConnectednessAnalyzer:
    """
    Analyzer for sentiment network connectedness.
    
    Implements the Diebold-Yilmaz connectedness framework adapted for
    entropy-based networks, per Cao et al. (2025).
    
    The analyzer can work with:
    - Granger causality networks
    - Transfer entropy networks
    - VAR-based forecast error variance decomposition
    
    Example:
        >>> analyzer = ConnectednessAnalyzer()
        >>> # From Granger causality network
        >>> gc_analyzer = GrangerCausalityAnalyzer()
        >>> gc_network = gc_analyzer.build_network(sentiment_df)
        >>> connectedness = analyzer.from_causality_network(gc_network)
        >>> print(f"Total Connectedness: {connectedness.total_connectedness:.1f}%")
    """
    
    def __init__(
        self,
        var_lag: int = 5,
        forecast_horizon: int = 10,
        generalized: bool = True
    ):
        """
        Initialize connectedness analyzer.
        
        Args:
            var_lag: Lag order for VAR model
            forecast_horizon: Forecast horizon for variance decomposition
            generalized: Use generalized FEVD (order-invariant)
        """
        self.var_lag = var_lag
        self.forecast_horizon = forecast_horizon
        self.generalized = generalized
    
    def from_causality_network(
        self,
        network: CausalityNetwork
    ) -> ConnectednessResult:
        """
        Calculate connectedness from a Granger causality network.
        
        Uses the significance-weighted adjacency matrix to compute
        spillover measures.
        
        Args:
            network: CausalityNetwork from GrangerCausalityAnalyzer
            
        Returns:
            ConnectednessResult with spillover measures
        """
        # Normalize adjacency matrix by row sums for percentage interpretation
        adj = network.adjacency_matrix.copy()
        
        # Calculate spillovers
        return self._calculate_spillovers(adj, network.nodes, "granger")
    
    def from_te_network(
        self,
        network: InformationFlowNetwork
    ) -> ConnectednessResult:
        """
        Calculate connectedness from a Transfer Entropy network.
        
        Args:
            network: InformationFlowNetwork from TransferEntropyAnalyzer
            
        Returns:
            ConnectednessResult with spillover measures
        """
        adj = network.adjacency_matrix.copy()
        return self._calculate_spillovers(adj, network.nodes, "transfer_entropy")
    
    def from_data(
        self,
        data: pd.DataFrame,
        columns: Optional[list[str]] = None,
        method: str = "var"
    ) -> ConnectednessResult:
        """
        Calculate connectedness directly from time series data.
        
        Args:
            data: DataFrame with sentiment time series
            columns: Columns to include
            method: "var" for VAR-based, "granger" for Granger-based, "te" for TE-based
            
        Returns:
            ConnectednessResult
        """
        if columns is None:
            columns = data.select_dtypes(include=[np.number]).columns.tolist()
        
        if method == "var":
            return self._var_connectedness(data[columns])
        elif method == "granger":
            gc_analyzer = GrangerCausalityAnalyzer(max_lag=self.var_lag)
            network = gc_analyzer.build_network(data, columns)
            return self.from_causality_network(network)
        elif method == "te":
            te_analyzer = TransferEntropyAnalyzer(history_length=3)
            network = te_analyzer.build_network(data, columns)
            return self.from_te_network(network)
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def _calculate_spillovers(
        self,
        adjacency: np.ndarray,
        node_names: list[str],
        source: str
    ) -> ConnectednessResult:
        """
        Calculate spillover measures from adjacency matrix.
        
        Implements Diebold-Yilmaz spillover measures adapted for
        entropy-based networks.
        """
        n = len(node_names)
        
        # Normalize adjacency for percentage interpretation
        # Row sums should represent total influence received
        row_sums = adjacency.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1  # Avoid division by zero
        
        normalized = adjacency / row_sums * 100  # Convert to percentages
        
        # Set diagonal to 0 (own contribution)
        np.fill_diagonal(normalized, 0)
        
        # Calculate spillover measures
        # TO: column sum (how much node j transmits to others)
        to_spillovers = normalized.sum(axis=0)
        
        # FROM: row sum (how much node i receives from others)
        from_spillovers = normalized.sum(axis=1)
        
        # Net: TO - FROM
        net_spillovers = to_spillovers - from_spillovers
        
        # Total Connectedness Index (TCI)
        # Average of off-diagonal elements
        total = normalized.sum() / n
        
        # Build dictionaries
        to_dict = {name: float(to_spillovers[i]) for i, name in enumerate(node_names)}
        from_dict = {name: float(from_spillovers[i]) for i, name in enumerate(node_names)}
        net_dict = {name: float(net_spillovers[i]) for i, name in enumerate(node_names)}
        
        return ConnectednessResult(
            total_connectedness=float(total),
            to_spillovers=to_dict,
            from_spillovers=from_dict,
            net_spillovers=net_dict,
            pairwise_spillovers=normalized,
            node_names=node_names,
            metadata={
                "method": source,
                "n_nodes": n,
            }
        )
    
    def _var_connectedness(self, data: pd.DataFrame) -> ConnectednessResult:
        """
        Calculate connectedness using VAR-based forecast error variance decomposition.
        
        Implements the generalized FEVD approach from Diebold-Yilmaz (2012).
        """
        try:
            from statsmodels.tsa.api import VAR
        except ImportError:
            logger.warning("statsmodels not available for VAR. Using Granger method.")
            gc_analyzer = GrangerCausalityAnalyzer(max_lag=self.var_lag)
            network = gc_analyzer.build_network(data)
            return self.from_causality_network(network)
        
        # Remove NaN and prepare data
        clean_data = data.dropna()
        
        if len(clean_data) < self.var_lag + 20:
            logger.warning("Insufficient data for VAR estimation.")
            return ConnectednessResult(
                total_connectedness=0.0,
                to_spillovers={col: 0.0 for col in data.columns},
                from_spillovers={col: 0.0 for col in data.columns},
                net_spillovers={col: 0.0 for col in data.columns},
                pairwise_spillovers=np.zeros((len(data.columns), len(data.columns))),
                node_names=list(data.columns),
                metadata={"method": "var", "error": "insufficient_data"}
            )
        
        try:
            # Fit VAR model
            model = VAR(clean_data)
            results = model.fit(maxlags=self.var_lag)
            
            # Get forecast error variance decomposition
            fevd = results.fevd(self.forecast_horizon)
            
            # Extract decomposition matrix at horizon H
            decomp = fevd.decomp[:, :, -1]  # Shape: (n_vars, n_vars)
            
            # Normalize rows to sum to 100
            row_sums = decomp.sum(axis=1, keepdims=True)
            decomp = decomp / row_sums * 100
            
            return self._calculate_spillovers(
                decomp, 
                list(data.columns),
                "var_fevd"
            )
            
        except Exception as e:
            logger.error(f"VAR estimation failed: {e}")
            gc_analyzer = GrangerCausalityAnalyzer(max_lag=self.var_lag)
            network = gc_analyzer.build_network(data)
            return self.from_causality_network(network)
    
    def dynamic_connectedness(
        self,
        data: pd.DataFrame,
        window_size: int = 30,
        step_size: int = 1,
        method: str = "granger"
    ) -> DynamicConnectedness:
        """
        Calculate dynamic connectedness over rolling windows.
        
        Per Cao et al. (2025), dynamic analysis reveals how sentiment
        transmission evolves over time and changes during market stress.
        
        Args:
            data: DataFrame with sentiment time series
            window_size: Size of rolling window
            step_size: Step size between windows
            method: Connectedness method to use
            
        Returns:
            DynamicConnectedness with time-varying measures
        """
        columns = data.select_dtypes(include=[np.number]).columns.tolist()
        
        dates = []
        total_conn = []
        net_spillovers = {col: [] for col in columns}
        
        n = len(data)
        
        for start in range(0, n - window_size + 1, step_size):
            end = start + window_size
            window_data = data.iloc[start:end]
            
            if window_data.isna().any().any():
                # Skip windows with NaN
                continue
            
            try:
                result = self.from_data(window_data, columns, method=method)
                
                dates.append(data.index[end - 1] if hasattr(data, 'index') else end - 1)
                total_conn.append(result.total_connectedness)
                
                for col in columns:
                    net_spillovers[col].append(result.net_spillovers.get(col, 0.0))
                    
            except Exception as e:
                logger.debug(f"Window {start}:{end} failed: {e}")
                continue
        
        return DynamicConnectedness(
            dates=dates,
            total_connectedness=total_conn,
            net_spillovers=net_spillovers,
            window_size=window_size
        )


def calculate_centrality(
    adjacency: np.ndarray,
    node_names: list[str]
) -> dict[str, dict[str, float]]:
    """
    Calculate network centrality measures.
    
    Returns:
        Dict with centrality measures for each node:
        - degree_in: In-degree centrality
        - degree_out: Out-degree centrality
        - betweenness: Betweenness centrality (approximated)
        - eigenvector: Eigenvector centrality
    """
    n = len(node_names)
    centrality = {}
    
    # Normalize adjacency
    max_val = adjacency.max()
    if max_val > 0:
        norm_adj = adjacency / max_val
    else:
        norm_adj = adjacency
    
    # In-degree: column sums
    in_degree = norm_adj.sum(axis=0)
    
    # Out-degree: row sums
    out_degree = norm_adj.sum(axis=1)
    
    # Total degree
    total_degree = in_degree + out_degree
    
    # Eigenvector centrality
    try:
        eigenvalues, eigenvectors = linalg.eig(norm_adj)
        max_idx = np.argmax(np.real(eigenvalues))
        eigenvector_cent = np.abs(np.real(eigenvectors[:, max_idx]))
        eigenvector_cent = eigenvector_cent / eigenvector_cent.max()  # Normalize
    except Exception:
        eigenvector_cent = np.ones(n) / n
    
    for i, name in enumerate(node_names):
        centrality[name] = {
            "degree_in": float(in_degree[i]),
            "degree_out": float(out_degree[i]),
            "degree_total": float(total_degree[i]),
            "eigenvector": float(eigenvector_cent[i]),
        }
    
    return centrality


def identify_key_transmitters(
    connectedness: ConnectednessResult,
    top_n: int = 3
) -> list[tuple[str, float]]:
    """
    Identify key sentiment transmitters in the network.
    
    Args:
        connectedness: ConnectednessResult from analyzer
        top_n: Number of top transmitters to return
        
    Returns:
        List of (node_name, net_spillover) tuples sorted by transmission strength
    """
    sorted_spillovers = sorted(
        connectedness.net_spillovers.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    return sorted_spillovers[:top_n]
