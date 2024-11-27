'use client'

import { useState, useEffect } from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'

interface Notification {
  id: string
  timestamp: string
  message: string
  severity: 'low' | 'medium' | 'high'
}

export default function AdminNotifications() {
  const [notifications, setNotifications] = useState<Notification[]>([])

  useEffect(() => {
    const eventSource = new EventSource(`${process.env.NEXT_PUBLIC_API_URL}/notifications/sse`)

    eventSource.onmessage = (event) => {
      if (event.data) {
        const newNotification = event.data
        setNotifications((prevNotifications) => [...prevNotifications, newNotification])
      }
    }

    return () => {
      eventSource.close()
    }
  }, [])

  return (
    <div className="w-full max-w-4xl mt-8">
    {notifications ? (
      notifications.map((notification) => (
      <Card key={notification.id} className="mb-4">
        <CardHeader>
          <CardTitle>JSON Results</CardTitle>
        </CardHeader>
        <CardContent>
          <pre className="whitespace-pre-wrap">{JSON.stringify(notification, null, 2)}</pre>
        </CardContent>
      </Card>
    ))):
    (<p>No notifications available.</p>)}
  </div>
  )
}

