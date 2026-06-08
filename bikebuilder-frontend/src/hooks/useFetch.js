import { useEffect } from "react";
import useAsync from "./useAsync";

const useFetch = (asyncFn, dependency, options = {}) => {
    const { skip = false } = options;
    const { data, loading, error, execute } = useAsync(asyncFn);

    useEffect(() => {
        if (skip) return;
        execute(dependency);
    }, [dependency, skip, execute]);

    return { data, loading, error, refetch: execute };
};

export default useFetch;
