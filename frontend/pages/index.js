import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4">
      <h1 className="text-4xl font-bold mb-4">BizDetails AI</h1>
      <p className="mb-8">Enriching Business Data with AI Precision</p>
      <Link href="/login" className="text-blue-500">Login</Link>
    </div>
  )
}
