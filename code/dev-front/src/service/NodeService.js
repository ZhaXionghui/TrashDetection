export default class NodeService {
    getModel1Nodes() {
        return fetch('demo/data/model1.json')
            .then((res) => res.json())
            .then((d) => d.root);
    }

    getTreeTableNodes() {
        return fetch('demo/data/treetablenodes.json')
            .then((res) => res.json())
            .then((d) => d.root);
    }

    getTreeNodes() {
        return fetch('demo/data/treenodes.json')
            .then((res) => res.json())
            .then((d) => d.root);
    }
}
