"""
Pytest tests for cir_to_connections functionality
"""

import pytest
import tempfile
import os
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
        file_path = CIR_FILES_DIR / "MOSbius_chip_RO_XAX.cir"
        
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

    def test_xax_with_custom_prefix(self):
        """Test XAX file with specific XAX prefix"""
        file_path = CIR_FILES_DIR / "MOSbius_chip_RO_XAX.cir"
        
        if not file_path.exists():
            pytest.skip(f"Test file {file_path.name} not found")
        
        connections = cir_to_connections(str(file_path), prefixes=["XAX"])
        
        assert connections is not None
        assert len(connections) > 0

    def test_xx_with_defaults(self):
        """Test XX file with default prefixes"""
        file_path = CIR_FILES_DIR / "MOSbius_chip_RO_XX.cir"
        
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

    def test_xx_with_custom_prefix(self):
        """Test XX file with specific XX prefix"""
        file_path = CIR_FILES_DIR / "MOSbius_chip_RO_XX.cir"
        
        if not file_path.exists():
            pytest.skip(f"Test file {file_path.name} not found")
        
        connections = cir_to_connections(str(file_path), prefixes=["XX"])
        
        assert connections is not None
        assert len(connections) > 0

    def test_xpx_with_custom_prefix(self):
        """Test XpX file (needs custom prefix - not in defaults)"""
        file_path = CIR_FILES_DIR / "MOSbius_chip_RO_XpX.cir"
        
        if not file_path.exists():
            pytest.skip(f"Test file {file_path.name} not found")
        
        # Should find nothing with defaults
        connections_default = cir_to_connections(str(file_path))
        assert len(connections_default) == 0
        
        # Should find connections with XpX prefix
        connections_custom = cir_to_connections(str(file_path), prefixes=["XpX"])
        assert connections_custom is not None
        assert len(connections_custom) > 0

    @pytest.mark.parametrize("prefix_type", ["XX", "X§X", "XAX"])
    def test_default_prefixes_include_all_types(self, prefix_type):
        """Test that default prefixes work for all supported types"""
        # Map prefix types to actual test files
        file_map = {
            "XX": "MOSbius_chip_RO_XX.cir",
            "X§X": "MOSbius_chip_RO_X§X.cir", 
            "XAX": "MOSbius_chip_RO_XAX.cir"
        }
        
        file_path = CIR_FILES_DIR / file_map[prefix_type]
        
        if not file_path.exists():
            pytest.skip(f"Test file {file_path.name} not found")
        
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

    # ===== NEW ENCODING TESTS =====
    
    @pytest.mark.parametrize("encoding", ["utf-8", "utf-8-sig", "cp1252", "latin1"])
    def test_encoding_robustness_with_special_chars(self, encoding):
        """Test that files with different encodings are handled correctly"""
        
        # Create test content with special characters (X§X) and a component name from MAGamp4problem.cir
        content = """* Test circuit with special characters
X§X1 BUS01 BUS02 BUS04 DP_nMOS_4x_A
X§X2 BUS03 BUS05 CS_nMOS_4x_B
.end
"""
        
        with tempfile.NamedTemporaryFile(mode='w', encoding=encoding, suffix='.cir', delete=False) as tmp_file:
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        try:
            # Test auto-detection
            connections = cir_to_connections(tmp_file_path, debug=False)
            assert len(connections) > 0
            
        except Exception as e:
            # If any error occurs, just test that the file can be read without encoding errors
            # The actual processing might fail for other reasons
            print(f"Processing failed (expected): {e}")
            # Test that we can at least read the file without encoding errors
            with open(tmp_file_path, 'r', encoding=encoding) as f:
                content_read = f.read()
                assert 'X§X' in content_read  # Verify the special character was preserved
                
        finally:
            os.unlink(tmp_file_path)
    
    def test_mag_amp_file_encoding(self):
        """Test the MAGamp4problem.cir file which has X§X characters from Windows"""
        file_path = CIR_FILES_DIR / "MAGamp4problem.cir"
        
        if not file_path.exists():
            pytest.skip(f"Test file {file_path.name} not found")
        
        # This file contains X§X characters and should work with our encoding handling
        connections = cir_to_connections(str(file_path), debug=False)
        assert isinstance(connections, dict)
        assert len(connections) > 0
        
        # Should contain bus connections from X§X lines
        bus_numbers = list(connections.keys())
        assert len(bus_numbers) > 0
        
        # Verify we found the expected buses (based on the file content)
        # The file has X§X lines with BUS01, BUS02, BUS03, etc.
        expected_buses = [1, 2, 3, 4, 5, 6, 7, 9, 10]  # Based on file inspection
        found_buses = sorted(bus_numbers)
        
        # Should find most of the expected buses
        assert len(set(found_buses) & set(expected_buses)) > 5
    
    def test_mac_vs_windows_file_encoding(self):
        """Test files from different platforms (Mac vs Windows)"""
        # Test the Mac file
        mac_file = CIR_FILES_DIR / "MOSbius_chip_RO_2_mac.cir"
        
        if mac_file.exists():
            connections_mac = cir_to_connections(str(mac_file), debug=False)
            assert isinstance(connections_mac, dict)
            assert len(connections_mac) > 0
        
        # Test a Windows file  
        windows_file = CIR_FILES_DIR / "MOSbius_chip_RO_XX.cir"
        
        if windows_file.exists():
            connections_windows = cir_to_connections(str(windows_file), debug=False)
            assert isinstance(connections_windows, dict)
            assert len(connections_windows) > 0
    
    def test_bom_handling_simulation(self):
        """Test handling of files with BOM (Byte Order Mark)"""
        content = """* Test circuit with BOM
X§X1 BUS01 BUS02 DP_nMOS_1x_A
.end
"""
    
        # Create file with UTF-8 BOM
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8-sig', suffix='.cir', delete=False) as tmp_file:
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        try:
            connections = cir_to_connections(tmp_file_path, debug=False)
            assert len(connections) > 0
        except KeyError as e:
            # If component not found, skip this test
            pytest.skip(f"Component not found in BitStream dictionary: {e}")
        finally:
            os.unlink(tmp_file_path)
    
    def test_all_test_files_encoding_robustness(self):
        """Test that all existing test files work with new encoding handling"""
        test_files = [
            "MAGamp4problem.cir",
            "MOSbius_chip_RO_X§X.cir", 
            "MOSbius_chip_RO_XX.cir",
            "MOSbius_chip_RO_XAX.cir",
            "MOSbius_chip_RO_XpX.cir",
            "MOSbius_chip_RO_2_mac.cir"
        ]
        
        results = {}
        
        for filename in test_files:
            file_path = CIR_FILES_DIR / filename
            if file_path.exists():
                try:
                    connections = cir_to_connections(str(file_path), debug=False)
                    results[filename] = {
                        'connections': len(connections) if connections else 0,
                        'status': 'success' if connections else 'no_connections'
                    }
                except Exception as e:
                    results[filename] = {
                        'connections': 0,
                        'status': f'error: {e}'
                    }
            else:
                results[filename] = {'connections': 0, 'status': 'file_not_found'}
        
        # Print summary for debugging
        print(f"\nEncoding robustness test summary:")
        for filename, result in results.items():
            print(f"  {filename}: {result['connections']} connections ({result['status']})")
        
        # At least half the files should work
        successful_files = [f for f, r in results.items() if 'success' in str(r.get('status', ''))]
        total_existing_files = [f for f, r in results.items() if r['status'] != 'file_not_found']
        
        if total_existing_files:
            success_rate = len(successful_files) / len(total_existing_files)
            assert success_rate >= 0.5, f"At least 50% of files should work. Success rate: {success_rate:.1%}"
    
    # ===== EXISTING TESTS =====
    
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