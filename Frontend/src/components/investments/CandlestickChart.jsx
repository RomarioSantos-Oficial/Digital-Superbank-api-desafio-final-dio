import React, { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';

/**
 * Componente de Gráfico de Velas (Candlestick Chart)
 * Exibe dados OHLCV em tempo real
 */
const CandlestickChart = ({ candles = [], symbol, width = 800, height = 400 }) => {
  const canvasRef = useRef(null);
  const [hoveredCandle, setHoveredCandle] = useState(null);

  useEffect(() => {
    if (!candles || candles.length === 0) return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    
    // Limpa canvas
    ctx.clearRect(0, 0, width, height);

    // Configurações
    const padding = { top: 40, right: 60, bottom: 60, left: 60 };
    const chartWidth = width - padding.left - padding.right;
    const chartHeight = height - padding.top - padding.bottom;

    // Encontra min/max de preços
    const prices = candles.flatMap(c => [c.high, c.low]);
    const maxPrice = Math.max(...prices);
    const minPrice = Math.min(...prices);
    const priceRange = maxPrice - minPrice;

    // Adiciona margem de 5%
    const margin = priceRange * 0.05;
    const adjustedMax = maxPrice + margin;
    const adjustedMin = minPrice - margin;
    const adjustedRange = adjustedMax - adjustedMin;

    // Escala Y (preço)
    const priceToY = (price) => {
      return padding.top + chartHeight - ((price - adjustedMin) / adjustedRange) * chartHeight;
    };

    // Largura de cada vela
    const candleWidth = Math.max(2, Math.min(20, chartWidth / candles.length * 0.7));
    const candleSpacing = chartWidth / candles.length;

    // Desenha grid
    ctx.strokeStyle = '#e5e7eb';
    ctx.lineWidth = 1;

    // Linhas horizontais (preços)
    const numGridLines = 5;
    for (let i = 0; i <= numGridLines; i++) {
      const price = adjustedMin + (adjustedRange / numGridLines) * i;
      const y = priceToY(price);

      ctx.beginPath();
      ctx.moveTo(padding.left, y);
      ctx.lineTo(width - padding.right, y);
      ctx.stroke();

      // Label do preço
      ctx.fillStyle = '#6b7280';
      ctx.font = '12px sans-serif';
      ctx.textAlign = 'right';
      ctx.fillText(`R$ ${price.toFixed(2)}`, padding.left - 10, y + 4);
    }

    // Desenha velas
    candles.forEach((candle, index) => {
      const x = padding.left + index * candleSpacing + candleSpacing / 2;

      const openY = priceToY(candle.open);
      const closeY = priceToY(candle.close);
      const highY = priceToY(candle.high);
      const lowY = priceToY(candle.low);

      const isGreen = candle.close >= candle.open;
      const color = isGreen ? '#10b981' : '#ef4444';

      // Desenha pavio (linha vertical)
      ctx.strokeStyle = color;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(x, highY);
      ctx.lineTo(x, lowY);
      ctx.stroke();

      // Desenha corpo da vela
      const bodyTop = Math.min(openY, closeY);
      const bodyHeight = Math.abs(closeY - openY);
      
      ctx.fillStyle = color;
      ctx.fillRect(
        x - candleWidth / 2,
        bodyTop,
        candleWidth,
        bodyHeight || 1 // Mínimo 1px se open === close
      );

      // Borda do corpo
      ctx.strokeStyle = color;
      ctx.lineWidth = 1;
      ctx.strokeRect(
        x - candleWidth / 2,
        bodyTop,
        candleWidth,
        bodyHeight || 1
      );
    });

    // Desenha eixos
    ctx.strokeStyle = '#1f2937';
    ctx.lineWidth = 2;

    // Eixo Y
    ctx.beginPath();
    ctx.moveTo(padding.left, padding.top);
    ctx.lineTo(padding.left, height - padding.bottom);
    ctx.stroke();

    // Eixo X
    ctx.beginPath();
    ctx.moveTo(padding.left, height - padding.bottom);
    ctx.lineTo(width - padding.right, height - padding.bottom);
    ctx.stroke();

    // Labels do eixo X (tempo)
    ctx.fillStyle = '#6b7280';
    ctx.font = '11px sans-serif';
    ctx.textAlign = 'center';

    const labelsToShow = Math.min(10, candles.length);
    const labelInterval = Math.floor(candles.length / labelsToShow) || 1;

    candles.forEach((candle, index) => {
      if (index % labelInterval === 0 || index === candles.length - 1) {
        const x = padding.left + index * candleSpacing + candleSpacing / 2;
        const time = new Date(candle.close_time);
        
        // Detecta intervalo baseado na diferença de tempo entre velas
        const timeDiff = index > 0 
          ? new Date(candles[index].close_time) - new Date(candles[index - 1].close_time)
          : 60000; // default 1 minuto

        // Formata label baseado no intervalo
        let label;
        if (timeDiff < 60000) {
          // Menor que 1 minuto: mostra hora:minuto:segundo
          label = time.toLocaleTimeString('pt-BR', { 
            hour: '2-digit', 
            minute: '2-digit',
            second: '2-digit'
          });
        } else if (timeDiff < 3600000) {
          // Menor que 1 hora: mostra hora:minuto
          label = time.toLocaleTimeString('pt-BR', { 
            hour: '2-digit', 
            minute: '2-digit' 
          });
        } else {
          // 1 hora ou mais: mostra hora:minuto e data se necessário
          label = time.toLocaleTimeString('pt-BR', { 
            hour: '2-digit', 
            minute: '2-digit' 
          });
        }

        ctx.fillText(label, x, height - padding.bottom + 20);
      }
    });

    // Título
    ctx.fillStyle = '#111827';
    ctx.font = 'bold 16px sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(symbol || 'Gráfico de Velas', padding.left, 25);

  }, [candles, width, height, symbol]);

  const handleMouseMove = (e) => {
    if (!candles || candles.length === 0) return;

    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const padding = { top: 40, right: 60, bottom: 60, left: 60 };
    const chartWidth = width - padding.left - padding.right;
    const candleSpacing = chartWidth / candles.length;

    const index = Math.floor((x - padding.left) / candleSpacing);

    if (index >= 0 && index < candles.length) {
      setHoveredCandle({ ...candles[index], index });
    } else {
      setHoveredCandle(null);
    }
  };

  const handleMouseLeave = () => {
    setHoveredCandle(null);
  };

  return (
    <div className="relative">
      <canvas
        ref={canvasRef}
        width={width}
        height={height}
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
        className="border border-gray-200 rounded-lg bg-white cursor-crosshair"
      />

      {/* Tooltip */}
      {hoveredCandle && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="absolute top-2 right-2 bg-white border border-gray-300 rounded-lg shadow-lg p-3 text-sm"
        >
          <div className="font-semibold text-gray-800 mb-2">
            {new Date(hoveredCandle.close_time).toLocaleString('pt-BR')}
          </div>
          <div className="space-y-1 text-xs">
            <div className="flex justify-between gap-4">
              <span className="text-gray-600">Abertura:</span>
              <span className="font-semibold">R$ {hoveredCandle.open.toFixed(2)}</span>
            </div>
            <div className="flex justify-between gap-4">
              <span className="text-gray-600">Máxima:</span>
              <span className="font-semibold text-green-600">R$ {hoveredCandle.high.toFixed(2)}</span>
            </div>
            <div className="flex justify-between gap-4">
              <span className="text-gray-600">Mínima:</span>
              <span className="font-semibold text-red-600">R$ {hoveredCandle.low.toFixed(2)}</span>
            </div>
            <div className="flex justify-between gap-4">
              <span className="text-gray-600">Fechamento:</span>
              <span className="font-semibold">R$ {hoveredCandle.close.toFixed(2)}</span>
            </div>
            <div className="flex justify-between gap-4 pt-1 border-t">
              <span className="text-gray-600">Volume:</span>
              <span className="font-semibold">{hoveredCandle.volume.toLocaleString('pt-BR')}</span>
            </div>
            {hoveredCandle.trades && (
              <div className="flex justify-between gap-4">
                <span className="text-gray-600">Negociações:</span>
                <span className="font-semibold">{hoveredCandle.trades}</span>
              </div>
            )}
          </div>
        </motion.div>
      )}

      {/* Legenda */}
      <div className="flex items-center justify-center gap-6 mt-4 text-sm">
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-green-500 rounded"></div>
          <span className="text-gray-600">Alta (Close ≥ Open)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-red-500 rounded"></div>
          <span className="text-gray-600">Baixa (Close &lt; Open)</span>
        </div>
      </div>
    </div>
  );
};

export default CandlestickChart;
