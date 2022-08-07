export const useUnits = () => {
  const units = [
    { text: 'Spannung (V)', value: 'voltage' },
    { text: 'Eingangsstrom (A)', value: 'input_current' },
    { text: 'Ausgangsstrom (A)', value: 'output_current' },
    { text: 'Ladezustand (Ah)', value: 'soc' },
  ]

  return units
}
