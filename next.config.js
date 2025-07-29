/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  basePath: process.env.NODE_ENV === 'production' ? '/ccdebug-landing' : '',
  assetPrefix: process.env.NODE_ENV === 'production' ? '/ccdebug-landing' : '',
  images: {
    unoptimized: true,
  },
  trailingSlash: true,
}

module.exports = nextConfig