import { IAnnotationModel, IJCadWorkerRegistry, IJupyterCadTracker } from '@jupytercad/schema';
import { JupyterFrontEndPlugin } from '@jupyterlab/application';
export declare const trackerPlugin: JupyterFrontEndPlugin<IJupyterCadTracker>;
export declare const annotationPlugin: JupyterFrontEndPlugin<IAnnotationModel>;
export declare const workerRegistryPlugin: JupyterFrontEndPlugin<IJCadWorkerRegistry>;
