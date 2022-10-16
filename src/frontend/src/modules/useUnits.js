export const useUnits = () => {
  const units = {
    voltage: { text: 'Spannung (V)', color: '#0000ff', unit: 'V' },
    input_current: { text: 'Eingangsstrom (A)', color: '#ff0000', unit: 'A' },
    output_current: { text: 'Ausgangsstrom (A)', color: '#ff0000', unit: 'A' },
    soc: { text: 'Ladezustand (Ah)', color: '#00ffff', unit: 'Ah' },
  }

  return units
}
