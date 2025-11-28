import { useState } from 'react'
import { Button } from './components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl">Vite + React + shadcn/ui</CardTitle>
          <CardDescription>
            A modern React starter with TypeScript and Tailwind CSS
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="text-center">
            <Button 
              onClick={() => setCount((count) => count + 1)}
              variant="default"
              size="lg"
              className="w-full"
            >
              Count is {count}
            </Button>
          </div>
          <div className="grid grid-cols-2 gap-2">
            <Button variant="outline" size="sm">
              Outline
            </Button>
            <Button variant="secondary" size="sm">
              Secondary
            </Button>
            <Button variant="destructive" size="sm">
              Destructive
            </Button>
            <Button variant="ghost" size="sm">
              Ghost
            </Button>
          </div>
          <p className="text-sm text-muted-foreground text-center">
            Edit <code className="bg-muted px-1 py-0.5 rounded text-xs">src/App.tsx</code> and save to test HMR
          </p>
        </CardContent>
      </Card>
    </div>
  )
}

export default App
