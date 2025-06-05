import java.util.*;

public class Grafo {
    private List<List<Integer>> listaAdjacencia;

    public Grafo(int numeroDeVertices) {
        listaAdjacencia = new ArrayList<>();
        for (int i = 0; i < numeroDeVertices; i++) {
            listaAdjacencia.add(new ArrayList<>());
        }
    }

    // Adiciona uma aresta entre dois vértices (grafo não direcionado)
    public void adicionarAresta(int origem, int destino) {
        listaAdjacencia.get(origem).add(destino);
        listaAdjacencia.get(destino).add(origem); // Remova esta linha se o grafo for direcionado
    }

    // Função pública que inicia a BFS
    public void buscaEmLargura(int verticeInicial) {
        boolean[] visitado = new boolean[listaAdjacencia.size()];
        Queue<Integer> fila = new LinkedList<>();

        visitado[verticeInicial] = true;
        fila.offer(verticeInicial);

        System.out.println("Iniciando BFS a partir do vértice " + verticeInicial + ":");

        while (!fila.isEmpty()) {
            int verticeAtual = fila.poll();
            visitar(verticeAtual);

            for (int vizinho : listaAdjacencia.get(verticeAtual)) {
                if (!visitado[vizinho]) {
                    visitado[vizinho] = true;
                    fila.offer(vizinho);
                }
            }
        }
    }

    // Apenas um exemplo de ação ao visitar um vértice
    private void visitar(int vertice) {
        System.out.println("Visitando vértice: " + vertice);
    }

    // Exemplo de uso
    public static void main(String[] args) {
        Grafo grafo = new Grafo(6);
        grafo.adicionarAresta(0, 1);
        grafo.adicionarAresta(0, 2);
        grafo.adicionarAresta(1, 3);
        grafo.adicionarAresta(1, 4);
        grafo.adicionarAresta(2, 5);

        grafo.buscaEmLargura(0);
    }
}
