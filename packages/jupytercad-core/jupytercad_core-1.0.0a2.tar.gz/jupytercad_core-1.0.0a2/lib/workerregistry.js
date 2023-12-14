export class JupyterCadWorkerRegistry {
    constructor() {
        this._registry = new Map();
    }
    registerWorker(workerId, worker) {
        if (!this._registry.has(workerId)) {
            this._registry.set(workerId, worker);
        }
        else {
            console.error('Worker is already registered!');
        }
    }
    unregisterWorker(workerId) {
        if (!this._registry.has(workerId)) {
            this._registry.delete(workerId);
        }
    }
    getWorker(workerId) {
        return this._registry.get(workerId);
    }
    getAllWorkers() {
        return [...this._registry.values()];
    }
}
