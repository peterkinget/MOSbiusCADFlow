"""
Pytest tests for cir_to_connections functionality
"""

import pytest
from pathlib import Path
import sys

# Add parent directory to path for local development
sys.path.insert(0, str(Path(__file__).parent.parent))

from MOSbiusTools.scripts.cir_to_connections import cir_to_connections

# Test data directory
TEST_DIR = Path(__file__).parent
CIR_FILES_DIR = TEST_DIR / "cir_files"

class TestCirToConnections:
    
    def test_x_section_x_with_defaults(self):
        """Test X§X file with default prefixes"""
        file_path = CIR_FILES_DIR / "MOSbius_chip_RO_X§X.cir"
        
        if not file_path.exists():
            pytest.skip(f"Test file {file_path.name} not found")
        
        connections = cir_to_connections(str(file_path))
        
        assert connections is not None
        assert len(connections) > 0
        assert isinstance(connections, dict)
        
        # Check that we have bus numbers as keys and pin lists as values
        for bus, pins in connections.items():
            assert isinstance(bus, int)
            assert isinstance(pins, list)
    
    def test_x_section_x_with_custom_prefix(self):
        """Test X§X file with specific prefix"""
        file_path = CIR_FILES_DIR / "MOSbius_chip_RO_X§X.cir"
        
        if not file_path.exists():
            pytest.skip(f"Test file {file_path.name} not found")
        
        connections = cir_to_connections(str(file_path), prefixes=["X§X"])
        
        assert connections is not None
        assert len(connections) > 0

    def test_xax_with_defaults(self):
        """Test XAX file with default prefixes"""
        # Look for XAX files in the directory
        xax_files = list(CIR_FILES_DIR.glob("*XAX*.cir"))
        
        if not xax_files:
            pytest.skip("No XAX .cir files found in test directory")
        
        file_path = xax_files[0]  # Use the first XAX file found
        connections = cir_to_connections(str(file_path))
        
        assert connections is not None
        assert len(connections) > 0
        assert isinstance(connections, dict)
        
        # Check that we have bus numbers as keys and pin lists as values
        for bus, pins in connections.items():
            assert isinstance(bus, int)
            assert isinstance(pins, list)

    def test_xax_with_custom_prefix(self):
        """Test XAX file with specific XAX prefix"""
        xax_files = list(CIR_FILES_DIR.glob("*XAX*.cir"))
        
        if not xax_files:
            pytest.skip("No XAX .cir files found in test directory")
        
        file_path = xax_files[0]
        connections = cir_to_connections(str(file_path), prefixes=["XAX"])
        
        assert connections is not None
        assert len(connections) > 0

    def test_xx_with_defaults(self):
        """Test XX file with default prefixes"""
        # Look for XX files (but not X§X or XAX files)
        xx_files = [f for f in CIR_FILES_DIR.glob("*XX*.cir") 
                   if "X§X" not in f.name and "XAX" not in f.name]
        
        if not xx_files:
            pytest.skip("No XX .cir files found in test directory")
        
        file_path = xx_files[0]
        connections = cir_to_connections(str(file_path))
        
        assert connections is not None
        assert len(connections) > 0
        assert isinstance(connections, dict)
        
        # Check that we have bus numbers as keys and pin lists as values
        for bus, pins in connections.items():
            assert isinstance(bus, int)
            assert isinstance(pins, list)

    def test_xx_with_custom_prefix(self):
        """Test XX file with specific XX prefix"""
        xx_files = [f for f in CIR_FILES_DIR.glob("*XX*.cir") 
                   if "X§X" not in f.name and "XAX" not in f.name]
        
        if not xx_files:
            pytest.skip("No XX .cir files found in test directory")
        
        file_path = xx_files[0]
        connections = cir_to_connections(str(file_path), prefixes=["XX"])
        
        assert connections is not None
        assert len(connections) > 0

    @pytest.mark.parametrize("prefix_type", ["XX", "X§X", "XAX"])
    def test_default_prefixes_include_all_types(self, prefix_type):
        """Test that default prefixes work for all supported types"""
        # Find a file with the specific prefix type
        if prefix_type == "X§X":
            test_files = list(CIR_FILES_DIR.glob("*X§X*.cir"))
        elif prefix_type == "XAX":
            test_files = list(CIR_FILES_DIR.glob("*XAX*.cir"))
        else:  # XX
            test_files = [f for f in CIR_FILES_DIR.glob("*XX*.cir") 
                         if "X§X" not in f.name and "XAX" not in f.name]
        
        if not test_files:
            pytest.skip(f"No {prefix_type} .cir files found in test directory")
        
        file_path = test_files[0]
        
        # Test with default prefixes (should include XX, X§X, XAX)
        connections_default = cir_to_connections(str(file_path))
        
        # Test with specific prefix
        connections_specific = cir_to_connections(str(file_path), prefixes=[prefix_type])
        
        # Both should find connections
        assert connections_default is not None
        assert connections_specific is not None
        assert len(connections_default) > 0
        assert len(connections_specific) > 0
        
        # Results should be the same since the file only contains one prefix type
        assert connections_default == connections_specific
    
    def test_wrong_prefix_returns_empty(self):
        """Test that wrong prefix returns no connections"""
        file_path = CIR_FILES_DIR / "MOSbius_chip_RO_X§X.cir"
        
        if not file_path.exists():
            pytest.skip(f"Test file {file_path.name} not found")
        
        connections = cir_to_connections(str(file_path), prefixes=["YY"])
        
        assert connections is not None
        assert len(connections) == 0
    
    def test_multiple_prefixes(self):
        """Test with multiple prefixes"""
        file_path = CIR_FILES_DIR / "MOSbius_chip_RO_X§X.cir"
        
        if not file_path.exists():
            pytest.skip(f"Test file {file_path.name} not found")
        
        connections = cir_to_connections(str(file_path), prefixes=["X§X", "XX", "XAX"])
        
        assert connections is not None
        assert len(connections) > 0
    
    @pytest.mark.parametrize("debug_mode", [True, False])
    def test_debug_mode(self, debug_mode):
        """Test both debug modes"""
        file_path = CIR_FILES_DIR / "MOSbius_chip_RO_X§X.cir"
        
        if not file_path.exists():
            pytest.skip(f"Test file {file_path.name} not found")
        
        connections = cir_to_connections(str(file_path), debug=debug_mode)
        
        assert connections is not None
        assert len(connections) > 0

    def test_all_available_cir_files(self):
        """Test all .cir files in the test directory"""
        cir_files = list(CIR_FILES_DIR.glob("*.cir"))
        
        if not cir_files:
            pytest.skip("No .cir files found in test directory")
        
        results = {}
        
        for file_path in cir_files:
            print(f"\nTesting {file_path.name}")
            
            # Test with default prefixes
            try:
                connections = cir_to_connections(str(file_path), debug=False)
                results[file_path.name] = {
                    'default_prefixes': len(connections) if connections else 0,
                    'status': 'success' if connections else 'no_connections'
                }
                print(f"  Default prefixes: {len(connections) if connections else 0} connections")
            except Exception as e:
                results[file_path.name] = {
                    'default_prefixes': 0,
                    'status': f'error: {e}'
                }
                print(f"  Default prefixes: Error - {e}")
        
        # Print summary
        print(f"\nSummary of {len(cir_files)} files tested:")
        for filename, result in results.items():
            print(f"  {filename}: {result['default_prefixes']} connections ({result['status']})")
        
        # At least one file should work
        successful_files = [f for f, r in results.items() if r['status'] == 'success']
        assert len(successful_files) > 0, "At least one .cir file should be processed successfully"

if __name__ == "__main__":
    # Run pytest when executed directly
    pytest.main([__file__, "-v"])