import { describe, expect, it, vi } from "vitest"
import { renderHook, act } from "@testing-library/react"
import { useApiCall } from "@/shared/hooks/useApiCall"

describe("useApiCall", () => {
    it("starts with idle state", () => {
        const fn = vi.fn()
        const { result } = renderHook(() => useApiCall(fn))
        expect(result.current.loading).toBe(false)
        expect(result.current.error).toBe("")
        expect(result.current.data).toBeNull()
    })

    it("sets loading during call", async () => {
        let resolve: (v: any) => void
        const fn = vi.fn(
            () =>
                new Promise<{ result: null; error: null }>((r) => {
                    resolve = r
                })
        )
        const { result } = renderHook(() => useApiCall(fn))

        act(() => {
            result.current.call()
        })
        expect(result.current.loading).toBe(true)

        await act(async () => {
            resolve!({ result: "data", error: null })
        })
        expect(result.current.loading).toBe(false)
    })

    it("returns result on success", async () => {
        const fn = vi.fn().mockResolvedValue({ result: { id: 1 }, error: null })
        const { result } = renderHook(() => useApiCall(fn))

        await act(async () => {
            await result.current.call()
        })

        expect(result.current.data).toEqual({ id: 1 })
        expect(result.current.error).toBe("")
    })

    it("sets error on failure", async () => {
        const fn = vi
            .fn()
            .mockResolvedValue({ result: null, error: "Not found" })
        const { result } = renderHook(() => useApiCall(fn))

        await act(async () => {
            await result.current.call()
        })

        expect(result.current.data).toBeNull()
        expect(result.current.error).toBe("Not found")
    })

    it("passes args to fn", async () => {
        const fn = vi.fn().mockResolvedValue({ result: null, error: "" })
        const { result } = renderHook(() => useApiCall(fn))

        await act(async () => {
            await result.current.call(42, "hello")
        })

        expect(fn).toHaveBeenCalledWith(42, "hello")
    })

    it("clears error on subsequent call", async () => {
        const fn = vi
            .fn()
            .mockResolvedValueOnce({ result: null, error: "fail" })
            .mockResolvedValueOnce({ result: "ok", error: null })
        const { result } = renderHook(() => useApiCall(fn))

        await act(async () => {
            await result.current.call()
        })
        expect(result.current.error).toBe("fail")

        await act(async () => {
            await result.current.call()
        })
        expect(result.current.error).toBe("")
    })
})
