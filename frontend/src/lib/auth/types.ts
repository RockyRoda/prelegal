export interface AuthUser {
  id: number;
  name: string;
  email: string;
}

export interface AuthSession {
  user: AuthUser;
  token: string;
}
