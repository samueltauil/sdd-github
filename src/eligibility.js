export function getEligibility({ authenticated, serviceDate, coverageStart, coverageEnd }) {
  if (!authenticated) throw new Error('Unauthorized');
  const requested = new Date(`${serviceDate}T00:00:00Z`);
  const start = new Date(`${coverageStart}T00:00:00Z`);
  const end = new Date(`${coverageEnd}T00:00:00Z`);
  return requested >= start && requested <= end ? 'Active' : 'Inactive';
}
