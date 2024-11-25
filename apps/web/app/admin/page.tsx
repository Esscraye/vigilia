import AdminNotifications from '../../components/AdminNotifications'

export default function AdminPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1 className="text-4xl font-bold mb-8">Admin Notifications</h1>
      <AdminNotifications />
    </main>
  )
}

