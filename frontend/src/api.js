import axios from "axios";
export const api = axios.create({ baseURL: "http://localhost:8000" });
export async function submitTrade(command) {
  const { data } = await api.post("/trade", { command });
  return data;
}
