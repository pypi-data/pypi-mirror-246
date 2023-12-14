import { AnnotationModel } from '@jupytercad/base';
import { OCC_WORKER_ID, OccWorker } from '@jupytercad/occ-worker';
import { IAnnotationToken, IJCadWorkerRegistryToken, IJupyterCadDocTracker } from '@jupytercad/schema';
import { WidgetTracker } from '@jupyterlab/apputils';
import { IMainMenu } from '@jupyterlab/mainmenu';
import { ITranslator } from '@jupyterlab/translation';
import { JupyterCadWorkerRegistry } from './workerregistry';
const NAME_SPACE = 'jupytercad';
export const trackerPlugin = {
    id: 'jupytercad:core:tracker',
    autoStart: true,
    requires: [ITranslator],
    optional: [IMainMenu],
    provides: IJupyterCadDocTracker,
    activate: (app, translator, mainMenu) => {
        const tracker = new WidgetTracker({
            namespace: NAME_SPACE
        });
        console.log('jupytercad:core:tracker is activated!');
        return tracker;
    }
};
export const annotationPlugin = {
    id: 'jupytercad:core:annotation',
    autoStart: true,
    requires: [IJupyterCadDocTracker],
    provides: IAnnotationToken,
    activate: (app, tracker) => {
        var _a;
        const annotationModel = new AnnotationModel({
            context: (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.context
        });
        tracker.currentChanged.connect((_, changed) => {
            annotationModel.context = (changed === null || changed === void 0 ? void 0 : changed.context) || undefined;
        });
        return annotationModel;
    }
};
export const workerRegistryPlugin = {
    id: 'jupytercad:core:worker-registry',
    autoStart: true,
    requires: [],
    provides: IJCadWorkerRegistryToken,
    activate: (app) => {
        const workerRegistry = new JupyterCadWorkerRegistry();
        const worker = new Worker(new URL('@jupytercad/occ-worker/lib/worker', import.meta.url));
        const occWorker = new OccWorker({ worker });
        workerRegistry.registerWorker(OCC_WORKER_ID, occWorker);
        return workerRegistry;
    }
};
