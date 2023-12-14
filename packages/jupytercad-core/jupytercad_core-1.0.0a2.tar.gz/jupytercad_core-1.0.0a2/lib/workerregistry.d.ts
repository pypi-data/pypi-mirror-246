import { IJCadWorker, IJCadWorkerRegistry } from '@jupytercad/schema';
export declare class JupyterCadWorkerRegistry implements IJCadWorkerRegistry {
    constructor();
    registerWorker(workerId: string, worker: IJCadWorker): void;
    unregisterWorker(workerId: string): void;
    getWorker(workerId: string): IJCadWorker | undefined;
    getAllWorkers(): IJCadWorker[];
    private _registry;
}
