import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Button,
  Box,
  Card,
  CardContent,
  Alert,
  CircularProgress
} from '@mui/material';
import { SelectChangeEvent } from '@mui/material/Select';
import { useFetch } from './hooks/useFetch';

interface ContainerDimensions {
  length: number;
  width: number;
  height: number;
}

interface OptimizeRequest {
  container: ContainerDimensions;
  sku: string;
  item_volume_margin?: number;
}

interface OptimizeResponse {
  max_count: number;
  leftover_percentage: number;
  container_volume: number;
  item_volume: number;
  item_details: {
    sku: string;
    name: string;
    dimensions: {
      length: number;
      width: number;
      height: number;
    };
    weight: number;
  };
}

interface Item {
  sku: string;
  name: string;
  length: number;
  width: number;
  height: number;
  weight: number;
}

function App() {
  const [containerDimensions, setContainerDimensions] = useState<ContainerDimensions>({
    length: 0,
    width: 0,
    height: 0
  });
  const [selectedSku, setSelectedSku] = useState<string>('');
  const [items, setItems] = useState<Item[]>([]);
  
  const apiUrl = '';
  
  const { data: optimizeResult, loading: optimizeLoading, error: optimizeError, execute: executeOptimize, reset: resetOptimize } = useFetch<OptimizeResponse>();
  const { data: itemsData, loading: itemsLoading, error: itemsError, execute: executeItemsFetch } = useFetch<Item[]>();

  useEffect(() => {
    executeItemsFetch(`${apiUrl}/api/items`);
  }, []);

  useEffect(() => {
    if (itemsData) {
      setItems(itemsData);
    }
  }, [itemsData]);

  const handleDimensionChange = (field: keyof ContainerDimensions) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const value = parseFloat(event.target.value) || 0;
    setContainerDimensions(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSkuChange = (event: SelectChangeEvent<string>) => {
    setSelectedSku(event.target.value);
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    
    if (containerDimensions.length <= 0 || containerDimensions.width <= 0 || containerDimensions.height <= 0) {
      return;
    }
    
    if (!selectedSku) {
      return;
    }

    resetOptimize();

    const requestData: OptimizeRequest = {
      container: containerDimensions,
      sku: selectedSku,
      item_volume_margin: 0.95
    };

    await executeOptimize(`${apiUrl}/api/optimize`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    });
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom align="center">
        Container Loading Optimizer
      </Typography>
      
      <Paper elevation={3} sx={{ p: 4, mb: 4 }}>
        <Typography variant="h5" component="h2" gutterBottom>
          Optimization Parameters
        </Typography>
        
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              <TextField
                sx={{ flex: 1, minWidth: '200px' }}
                label="Container Length (cm)"
                type="number"
                value={containerDimensions.length || ''}
                onChange={handleDimensionChange('length')}
                inputProps={{ min: 0, step: 0.1 }}
                required
              />
              
              <TextField
                sx={{ flex: 1, minWidth: '200px' }}
                label="Container Width (cm)"
                type="number"
                value={containerDimensions.width || ''}
                onChange={handleDimensionChange('width')}
                inputProps={{ min: 0, step: 0.1 }}
                required
              />
              
              <TextField
                sx={{ flex: 1, minWidth: '200px' }}
                label="Container Height (cm)"
                type="number"
                value={containerDimensions.height || ''}
                onChange={handleDimensionChange('height')}
                inputProps={{ min: 0, step: 0.1 }}
                required
              />
            </Box>
            
            <FormControl fullWidth required>
              <InputLabel>Item SKU</InputLabel>
              <Select
                value={selectedSku}
                label="Item SKU"
                onChange={handleSkuChange}
                disabled={itemsLoading}
              >
                {items.map((item) => (
                  <MenuItem key={item.sku} value={item.sku}>
                    {item.sku} - {item.name} ({item.length}×{item.width}×{item.height} cm, {item.weight} kg)
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            
            <Button
              type="submit"
              variant="contained"
              size="large"
              disabled={optimizeLoading || itemsLoading}
              sx={{ mt: 2 }}
            >
              {optimizeLoading ? <CircularProgress size={24} /> : 'Optimize Loading'}
            </Button>
          </Box>
        </Box>
      </Paper>

      {(optimizeError || itemsError) && (
        <Alert severity="error" sx={{ mb: 4 }}>
          {optimizeError || itemsError}
        </Alert>
      )}

      {optimizeResult && (
        <Card elevation={3}>
          <CardContent>
            <Typography variant="h5" component="h3" gutterBottom>
              Optimization Results
            </Typography>
            
            <Box sx={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
              <Box sx={{ flex: 1, minWidth: '250px' }}>
                <Typography variant="h6" color="primary">
                  Maximum Items: {optimizeResult.max_count}
                </Typography>
                <Typography variant="body1">
                  Leftover Space: {optimizeResult.leftover_percentage.toFixed(2)}%
                </Typography>
                <Typography variant="body1">
                  Container Volume: {optimizeResult.container_volume.toLocaleString()} cm³
                </Typography>
                <Typography variant="body1">
                  Item Volume: {optimizeResult.item_volume.toLocaleString()} cm³
                </Typography>
              </Box>
              
              <Box sx={{ flex: 1, minWidth: '250px' }}>
                <Typography variant="h6" gutterBottom>
                  Item Details
                </Typography>
                <Typography variant="body1">
                  <strong>SKU:</strong> {optimizeResult.item_details.sku}
                </Typography>
                <Typography variant="body1">
                  <strong>Name:</strong> {optimizeResult.item_details.name}
                </Typography>
                <Typography variant="body1">
                  <strong>Dimensions:</strong> {optimizeResult.item_details.dimensions.length}×{optimizeResult.item_details.dimensions.width}×{optimizeResult.item_details.dimensions.height} cm
                </Typography>
                <Typography variant="body1">
                  <strong>Weight:</strong> {optimizeResult.item_details.weight} kg
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>
      )}
    </Container>
  );
}

export default App;
