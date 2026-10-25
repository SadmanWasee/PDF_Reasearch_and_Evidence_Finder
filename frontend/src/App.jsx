
import { useState } from 'react'

function App() {
  const [file, setFile] = useState(null)
  const [query, setQuery] = useState('')
  const [method, setMethod] = useState('hybrid')

  const [document, setDocument] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [uploadError, setUploadError] = useState('')

  function handleFileChange(event) {
    const selectedFile = event.target.files?.[0] ?? null

    setFile(selectedFile)
    setDocument(null)
    setUploadError('')

    if (!selectedFile) return

    if (
      !selectedFile.name.toLowerCase().endsWith('.pdf') ||
      selectedFile.type === 'application/x-msdownload'
    ) {
      setFile(null)
      setUploadError('Please select a valid PDF file.')
      return
    }

    if (selectedFile.size > 10 * 1024 * 1024) {
      setFile(null)
      setUploadError('The PDF must be smaller than 10 MB.')
    }
  }

  async function handleUpload() {
    if (!file) {
      setUploadError('Please select a PDF first.')
      return
    }

    setUploading(true)
    setUploadError('')
    setDocument(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch(
        'http://127.0.0.1:8000/upload',
        {
          method: 'POST',
          body: formData,
        },
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data.detail || 'The PDF upload failed.',
        )
      }

      setDocument(data)
    } catch (error) {
      setUploadError(
        error.message ||
          'Could not connect to the backend. Make sure FastAPI is running.',
      )
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      {/* Navigation */}
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div>
            <h1 className="text-xl font-bold tracking-tight text-indigo-700">
              Evidence Finder
            </h1>
            <p className="text-sm text-slate-500">
              Research smarter. Find evidence faster.
            </p>
          </div>

          <span className="hidden rounded-full bg-indigo-50 px-3 py-1 text-sm font-medium text-indigo-700 sm:inline-block">
            AI Research Assistant
          </span>
        </div>
      </header>

      <main className="mx-auto max-w-4xl px-6 py-12">
        {/* Hero */}
        <div className="mb-10 text-center">
          <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-indigo-100 bg-indigo-50 px-3 py-1 text-sm font-medium text-indigo-700">
            <span>✦</span>
            Intelligent Research Search
          </div>

          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Find evidence in your research papers
          </h2>

          <p className="mx-auto mt-3 max-w-2xl text-slate-600">
            Upload a research paper and discover relevant
            passages using keyword and semantic retrieval.
          </p>
        </div>

        {/* Main form */}
        <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
          {/* PDF upload */}
          <div>
            <div className="flex items-center gap-3">
              <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-indigo-50 font-semibold text-indigo-700">
                1
              </span>

              <div>
                <h3 className="text-lg font-semibold">
                  Upload a research paper
                </h3>
                <p className="text-sm text-slate-500">
                  PDF format · Maximum size 10 MB
                </p>
              </div>
            </div>

            <label className="mt-5 flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-slate-300 bg-slate-50 px-6 py-10 text-center transition hover:border-indigo-400 hover:bg-indigo-50">
              <span className="text-4xl">📄</span>

              <span className="mt-3 max-w-full break-all font-medium">
                {file ? file.name : 'Choose a PDF file'}
              </span>

              <span className="mt-1 text-sm text-slate-500">
                Click to browse your files
              </span>

              <input
                type="file"
                accept=".pdf,application/pdf"
                className="hidden"
                onChange={handleFileChange}
                disabled={uploading}
              />
            </label>

            <button
              type="button"
              onClick={handleUpload}
              disabled={!file || uploading}
              className="mt-4 w-full rounded-xl bg-indigo-600 px-5 py-3 font-semibold text-white transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:bg-slate-300"
            >
              {uploading ? 'Uploading PDF...' : 'Upload PDF'}
            </button>

            {uploadError && (
              <div
                role="alert"
                className="mt-4 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700"
              >
                {uploadError}
              </div>
            )}

            {document && (
              <div
                role="status"
                className="mt-4 rounded-xl border border-emerald-200 bg-emerald-50 p-4"
              >
                <p className="font-semibold text-emerald-800">
                  PDF uploaded successfully!
                </p>

                <p className="mt-1 wrap-break-word text-sm text-emerald-700">
                  {document.filename}
                </p>

                <div className="mt-3 flex flex-wrap gap-2">
                  <span className="rounded-lg bg-white px-3 py-2 text-sm text-emerald-800">
                    {document.page_count} pages
                  </span>

                  <span className="rounded-lg bg-white px-3 py-2 text-sm text-emerald-800">
                    {document.chunk_count} chunks
                  </span>
                </div>
              </div>
            )}
          </div>

          <div className="my-8 border-t border-slate-100" />

          {/* Research question */}
          <div>
            <div className="flex items-center gap-3">
              <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-indigo-50 font-semibold text-indigo-700">
                2
              </span>

              <h3 className="text-lg font-semibold">
                Ask a research question
              </h3>
            </div>

            <textarea
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Example: How are scientific claims verified?"
              rows={3}
              className="mt-4 w-full resize-y rounded-xl border border-slate-300 px-4 py-3 outline-none transition placeholder:text-slate-400 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100"
            />
          </div>

          <div className="my-8 border-t border-slate-100" />

          {/* Search method */}
          <div>
            <div className="flex items-center gap-3">
              <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-indigo-50 font-semibold text-indigo-700">
                3
              </span>

              <h3 className="text-lg font-semibold">
                Choose a search method
              </h3>
            </div>

            <div className="mt-4 grid gap-3 sm:grid-cols-3">
              {[
                {
                  value: 'bm25',
                  label: 'BM25',
                  description: 'Keyword matching',
                },
                {
                  value: 'semantic',
                  label: 'Semantic',
                  description: 'Meaning-based search',
                },
                {
                  value: 'hybrid',
                  label: 'Hybrid',
                  description: 'Combines both methods',
                },
              ].map((option) => (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => setMethod(option.value)}
                  aria-pressed={method === option.value}
                  className={`rounded-xl border p-4 text-left transition ${
                    method === option.value
                      ? 'border-indigo-500 bg-indigo-50 ring-2 ring-indigo-100'
                      : 'border-slate-200 hover:border-slate-400'
                  }`}
                >
                  <span className="block font-semibold">
                    {option.label}
                  </span>

                  <span className="mt-1 block text-sm text-slate-500">
                    {option.description}
                  </span>
                </button>
              ))}
            </div>
          </div>

          {/* Search button: wired up in the next step */}
          <button
            type="button"
            disabled={!document || !query.trim()}
            onClick={() =>
              alert(
                'PDF upload is ready! Next, we will connect the search API.',
              )
            }
            className="mt-8 w-full rounded-xl bg-indigo-600 px-5 py-3 font-semibold text-white transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:bg-slate-300"
          >
            Search research paper
          </button>

          {!document && (
            <p className="mt-3 text-center text-xs text-slate-500">
              Upload your PDF before searching its contents.
            </p>
          )}
        </section>

        {/* Footer */}
        <footer className="mt-8 text-center text-sm text-slate-500">
          <p>
            Evidence Finder · AI-powered research assistance
          </p>
          <p className="mt-1">
            Find relevant passages and trace them to their source pages.
          </p>
        </footer>
      </main>
    </div>
  )
}

export default App
