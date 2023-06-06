/** @type {import('next').NextConfig} */
const nextConfig = {
    env:{
        
    },
    images: {
        remotePatterns: [
          {
            protocol: 'https',
            hostname: 'i.scdn.co',
            port: '',
            pathname: '/image/**',
          },
        ],
      }
}

module.exports = nextConfig
