/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['i.scdn.co'], // Spotify image domain
  },
  // For Vercel deployment with monorepo structure
  trailingSlash: true,
  output: 'standalone',
  // API configuration for backend integration
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.NEXT_PUBLIC_API_URL 
          ? `${process.env.NEXT_PUBLIC_API_URL}/api/:path*`
          : 'http://localhost:8000/api/:path*'
      }
    ]
  }
}

module.exports = nextConfig
