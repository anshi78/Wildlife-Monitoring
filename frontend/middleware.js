import { NextResponse } from 'next/server';

// Temporarily bypassed to prevent missing Clerk API key errors.
// If you want to enable auth, add NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY and CLERK_SECRET_KEY
// to your .env.local file, and replace this dummy middleware with the Clerk setup.

export default function middleware() {
  return NextResponse.next();
}

/* --- CLERK MIDDLEWARE CODE ---
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';

const isProtectedRoute = createRouteMatcher([
  '/dashboard(.*)',
]);

export default clerkMiddleware(async (auth, req) => {
  if (isProtectedRoute(req)) {
    await auth.protect();
  }
});
---------------------------------*/

export const config = {
  matcher: [
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    '/(api|trpc)(.*)',
  ],
};
