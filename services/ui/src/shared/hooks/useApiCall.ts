import type { ApiResponse } from "@/shared/types/api"
import { useState } from "react"

export function useApiCall<TArgs extends unknown[], TResult>(
    fn: (...args: TArgs) => Promise<ApiResponse<TResult>>
) {
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")
    const [data, setData] = useState<TResult | null>(null)

    const call = async (...args: TArgs): Promise<TResult | null> => {
        setError("")
        setLoading(true)
        const { result, error } = await fn(...args)
        setLoading(false)
        if (error) setError(error)
        setData(result)
        return result
    }

    return { loading, error, data, call }
}
