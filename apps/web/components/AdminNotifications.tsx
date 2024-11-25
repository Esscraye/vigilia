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
    const eventSource = new EventSource('/api/notifications/sse')

    eventSource.onmessage = (event) => {
      const newNotification = JSON.parse(event.data)
      setNotifications((prevNotifications) => [...prevNotifications, newNotification])
    }

    return () => {
      eventSource.close()
    }
  }, [])

  return (
    <div className="w-full max-w-4xl">
      {notifications.map((notification) => (
        <Card key={notification.id} className="mb-4">
          <CardHeader>
            <CardTitle>
              <span className={`font-bold ${
                notification.severity === 'low' ? 'text-green-500' :
                notification.severity === 'medium' ? 'text-yellow-500' : 'text-red-500'
              }`}>
                {notification.severity.toUpperCase()} SEVERITY
              </span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p><strong>Timestamp:</strong> {notification.timestamp}</p>
            <p><strong>Message:</strong> {notification.message}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}

