"""
Test the actual cir_to_connections script (not just the function)
"""

import pytest
import subprocess
import tempfile
import json
import os
from pathlib import Path

# Test data directory
TEST_DIR = Path(__file__).parent
CIR_FILES_DIR = TEST_DIR / "cir_files"

class TestCirToConnectionsScript:
    
    def test_script_help(self):
        """Test that script shows help and includes prefixes option"""
        result = subprocess.run([
            'cir_to_connections', '--help'
        ], capture_output=True, text=True)
        
        assert result.returncode == 0
        assert '--prefixes' in result.stdout
        assert 'XX,X§X,XAX' in result.stdout  # Check default value
    
    def test_script_with_x_section_x_default(self):
        """Test script with X§X file using default prefixes"""
        file_path = CIR_FILES_DIR / "MOSbius_chip_RO_X§X.cir"
        
        if not file_path.exists():
            pytest.skip(f"Test file {file_path.name} not found")
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
            try:
                result = subprocess.run([
                    'cir_to_connections',
                    '-i', str(file_path),
                    '-o', tmp_file.name
                ], capture_output=True, text=True)
                
                assert result.returncode == 0, f"Script failed: {result.stderr}"
                
                # Check output file was created and has content
                assert os.path.exists(tmp_file.name)
                
                with open(tmp_file.name, 'r') as f:
                    connections = json.load(f)
                
                assert isinstance(connections, dict)
                assert len(connections) > 0
                
            finally:
                if os.path.exists(tmp_file.name):
                    os.unlink(tmp_file.name)
    
    def test_script_with_custom_prefix(self):
        """Test script with custom prefix"""
        file_path = CIR_FILES_DIR / "MOSbius_chip_RO_X§X.cir"
        
        if not file_path.exists():
            pytest.skip(f"Test file {file_path.name} not found")
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
            try:
                result = subprocess.run([
                    'cir_to_connections',
                    '-i', str(file_path),
                    '-o', tmp_file.name,
                    '-p', 'X§X'
                ], capture_output=True, text=True)
                
                assert result.returncode == 0, f"Script failed: {result.stderr}"
                
                with open(tmp_file.name, 'r') as f:
                    connections = json.load(f)
                
                assert len(connections) > 0
                
            finally:
                if os.path.exists(tmp_file.name):
                    os.unlink(tmp_file.name)
    
    def test_script_with_wrong_prefix(self):
        """Test script with wrong prefix should create empty connections"""
        file_path = CIR_FILES_DIR / "MOSbius_chip_RO_X§X.cir"
        
        if not file_path.exists():
            pytest.skip(f"Test file {file_path.name} not found")
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
            try:
                result = subprocess.run([
                    'cir_to_connections',
                    '-i', str(file_path),
                    '-o', tmp_file.name,
                    '-p', 'YY'  # Wrong prefix
                ], capture_output=True, text=True)
                
                assert result.returncode == 0, f"Script failed: {result.stderr}"
                
                with open(tmp_file.name, 'r') as f:
                    connections = json.load(f)
                
                assert len(connections) == 0
                
            finally:
                if os.path.exists(tmp_file.name):
                    os.unlink(tmp_file.name)
    
    @pytest.mark.parametrize("prefix_combo", [
        "XX",
        "X§X", 
        "XAX",
        "XX,X§X",
        "XX,X§X,XAX",
        "X§X,YY"  # Mix of valid and invalid
    ])
    def test_script_with_various_prefix_combinations(self, prefix_combo):
        """Test script with various prefix combinations"""
        file_path = CIR_FILES_DIR / "MOSbius_chip_RO_X§X.cir"
        
        if not file_path.exists():
            pytest.skip(f"Test file {file_path.name} not found")
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
            try:
                result = subprocess.run([
                    'cir_to_connections',
                    '-i', str(file_path),
                    '-o', tmp_file.name,
                    '-p', prefix_combo
                ], capture_output=True, text=True)
                
                assert result.returncode == 0, f"Script failed with {prefix_combo}: {result.stderr}"
                
                with open(tmp_file.name, 'r') as f:
                    connections = json.load(f)
                
                # Should find connections if X§X is in the prefix combo
                if 'X§X' in prefix_combo:
                    assert len(connections) > 0, f"Should find connections with {prefix_combo}"
                
            finally:
                if os.path.exists(tmp_file.name):
                    os.unlink(tmp_file.name)
    
    def test_script_debug_mode(self):
        """Test script with debug mode"""
        file_path = CIR_FILES_DIR / "MOSbius_chip_RO_X§X.cir"
        
        if not file_path.exists():
            pytest.skip(f"Test file {file_path.name} not found")
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
            try:
                result = subprocess.run([
                    'cir_to_connections',
                    '-i', str(file_path),
                    '-o', tmp_file.name,
                    '-d'  # Debug mode
                ], capture_output=True, text=True)
                
                assert result.returncode == 0, f"Script failed: {result.stderr}"
                
                # Debug mode should produce some output
                assert len(result.stdout) > 0 or len(result.stderr) > 0
                
                with open(tmp_file.name, 'r') as f:
                    connections = json.load(f)
                
                assert len(connections) > 0
                
            finally:
                if os.path.exists(tmp_file.name):
                    os.unlink(tmp_file.name)
    
    def test_script_missing_file(self):
        """Test script behavior with missing input file"""
        result = subprocess.run([
            'cir_to_connections',
            '-i', 'nonexistent_file.cir',
            '-o', 'output.json'
        ], capture_output=True, text=True)
        
        # Should fail with non-zero exit code
        assert result.returncode != 0
    
    def test_script_shows_help_with_no_args(self):
        """Test that script shows help when run with no arguments"""
        result = subprocess.run([
            'cir_to_connections'
        ], capture_output=True, text=True)
        
        # Your script is designed to show help when no args provided
        assert result.returncode == 0
        assert 'usage:' in result.stdout
        assert '--prefixes' in result.stdout

if __name__ == "__main__":
    pytest.main([__file__, "-v"])