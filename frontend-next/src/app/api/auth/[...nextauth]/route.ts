import NextAuth from 'next-auth';
import SpotifyProvider from 'next-auth/providers/spotify';

declare module 'next-auth' {
  /**
   * Returned by `useSession`, `getSession` and received as a prop on the `SessionProvider` React Context
   */
  interface Session {
    accessToken?: string;
  }
}

const handler = NextAuth({
  providers: [
    SpotifyProvider({
      authorization: {
        params: {
          scope: 'user-read-email,user-library-read',
          show_dialog: true,
        },
      },
      clientId: process.env.SPOTIFY_CLIENT!,
      clientSecret: process.env.SPOTIFY_SECRET!,
    }),
  ],
  callbacks: {
    async jwt({ token, account }) {
      // Persist the OAuth access_token to the token right after signin
      if (account) {
        token.accessToken = account.access_token;
      }
      return token;
    },
    async session({ session, token, user }) {
      // Send properties to the client, like an access_token from a provider.

      session.accessToken = token.accessToken as string;
      return session;
    },
  },
  pages: {
    signIn: '/',
  },
});

export { handler as GET, handler as POST };
