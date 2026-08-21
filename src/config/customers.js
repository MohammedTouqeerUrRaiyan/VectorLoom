export const DEMO_CUSTOMERS = [
  {
    username: "Touqeer",
    password: "password123",
    customerId:
      "75c54a755b8a467e53e0a4e01833deb029734feb22ad25438137925123a38f8b",
  },
];

export function authenticateCustomer(username, password) {
  return DEMO_CUSTOMERS.find(
    (customer) =>
      customer.username.toLowerCase() === username.trim().toLowerCase() &&
      customer.password === password
  );
}