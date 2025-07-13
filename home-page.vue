<template>
  <div class="home-page">
    <header-component />

    <main class="main-content">
      <!-- ─────────── área logado ─────────── -->
      <div v-if="authState.isLoggedIn">
        <h1>Bem-vindo, {{ authState.user.name }}!</h1>
        <p>Carregue as imagens necessárias para o sistema:</p>

        <!-- upload -->
        <div class="image-uploader">
          <!-- Imagem ANTES -->
          <label class="custom-file-upload">
            <input
              type="file"
              accept="image/*"
              @change="(e) => handleImageUpload(e, 'before')"
            />
            Imagem antes do processamento
          </label>
          <p v-if="imageNames.before">Imagem antes: {{ imageNames.before }}</p>
          <img
            v-if="preview.before"
            :src="preview.before"
            alt="Preview antes"
            class="preview-img"
          />
          
          <!-- Imagem DEPOIS -->
          <label class="custom-file-upload">
            <input
              type="file"
              accept="image/*"
              @change="(e) => handleImageUpload(e, 'after')"
            />
            Imagem depois do processamento
          </label>
          <p v-if="imageNames.after">Imagem depois: {{ imageNames.after }}</p>
          <img
            v-if="preview.after"
            :src="preview.after"
            alt="Preview depois"
            class="preview-img"
          />
        </div>

        <!-- Se ambas as imagens estiverem carregadas, mostra o menu de categorias -->
        <div v-if="imageNames.before && imageNames.after" class="algorithms-container">
          <h2>Selecione um algoritmo para aplicar:</h2>

          <div
            v-for="(cat, idx) in algorithmCategories"
            :key="cat.category"
            class="category-section"
          >
            <!-- Cabeçalho clicável para expandir/colapsar -->
            <div
              class="category-header"
              @click="expanded[idx] = !expanded[idx]"
            >
              <span>{{ cat.category }}</span>
              <span class="toggle-icon">
                {{ expanded[idx] ? '▾' : '▸' }}
              </span>
            </div>

            <!-- Lista de botões visível se expanded[idx] == true -->
            <div v-if="expanded[idx]" class="category-items">
              <button
                v-for="alg in cat.items"
                :key="alg.name"
                class="styled-button alg-button"
                @click="submitImages(alg.name)"
              >
                {{ alg.label }}
              </button>
            </div>
          </div>
        </div>

        <!-- resultado -->
        <div v-if="result" class="result-box">
          <p>RMSE: {{ result.rmse.toFixed(3) }}</p>
          <p v-if="result.success" class="success">
            Parabéns! Similaridade atingida.
          </p>
          <p v-else class="error">
            Você não atingiu a similaridade necessária. Tente novamente.
          </p>
          <pre v-if="result.sourceCode" class="code-block">
            <code v-html="highlightedCode"></code>
          </pre>
        </div>
      </div>

      <!-- ─────────── área não logado ─────────── -->
      <div v-else>
        <h1>Bem-vindo ao Sistema PDI</h1>
        <p>
          <router-link to="/login">Login</router-link> ou
          <router-link to="/register">Registrar-se</router-link>
        </p>
      </div>
    </main>

    <footer-component />
  </div>
</template>

<script>
import { inject, ref, computed } from 'vue';
import HeaderComponent from '../components/header-component.vue';
import FooterComponent from '../components/footer-component.vue';

/* ─── PrismJS para realce de sintaxe ─── */
import Prism from 'prismjs';
import 'prismjs/components/prism-python';
import 'prismjs/themes/prism-tomorrow.css';

/**
 * Estrutura de categorias/algoritmos.
 * Cada categoria possui um título e um array de objetos { name, label }.
 * O name deve corresponder ao nome do script Python/back-end.
 * O label é apenas para exibir no botão.
 */

const algorithmCategories = [
  {
    category: 'Ponto a Ponto',
    items: [
      { name: 'negative', label: 'Algoritmo Negativo' },
      { name: 'grayscale', label: 'Agoritmo Tons de Cinza' },
    ],
  },
  {
    category: 'Histograma',
    items: [
      { name: 'hist_equalization', label: 'Algoritmo Equalizar Histograma' },
    ],
  },
  {
    category: 'Filtragem Espacial',
    items: [
      { name: 'sobel', label: 'Algoritmo Sobel' },
      { name: 'mean_filter', label: 'Algoritmo Filtro Média'},
      { name: 'gaussian_blur', label: 'Algoritmo Suavização Gaussiana'},
      { name: 'sharpen', label: 'Algoritmo Filtro de Realce' },
      { name: 'unsharp_mask', label: 'Algoritmo Filtro de Realce Genérico'},
    ],
  },
  {
    category: 'Segmentação',
    items: [
      { name: 'otsu', label: 'Algoritmo OTSU' },
      { name: 'canny', label: 'Algoritmo Canny'},
    ],
  },
  {
    category: 'Transformações Geométricas',
    items: [
      { name: 'mirror', label: 'Algoritmo Espelhamento' },
      { name: 'transpose', label: 'Algoritmo Transposta'},
      { name: 'rotate', label: 'Algoritmo Rotação (90° por Padrão)'},
    ]
  }
];

export default {
  components: { HeaderComponent, FooterComponent },

  setup() {
    /* ---- estado global de autenticação ---- */
    const authState = inject('authState');

    /* ---- estado local da página ---- */
    const rawImages = ref({ before: null, after: null });
    const imageNames = ref({ before: null, after: null });
    const preview = ref({ before: null, after: null });
    const result = ref(null);

    /* ---- estado para expandir/colapsar categorias ---- */
    // Cada índice refere-se a algorithmCategories[idx].
    // Se true → categoria aberta; se false → categoria fechada.
    const expanded = ref(algorithmCategories.map(() => false));

    /* ---- upload das imagens ---- */
    const handleImageUpload = (event, type) => {
      const file = event.target.files[0];
      if (file) {
        rawImages.value[type] = file;
        imageNames.value[type] = file.name;
        if (preview.value[type]) URL.revokeObjectURL(preview.value[type]);
        preview.value[type] = URL.createObjectURL(file);
        // Sempre limpa resultado anterior quando troca uma imagem
        result.value = null;
      }
    };

    /* ---- submit ao backend ---- */
    const submitImages = async (algorithm) => {
      if (!rawImages.value.before || !rawImages.value.after) {
        alert('Por favor, carregue ambas as imagens antes de enviar.');
        return;
      }

      const formData = new FormData();
      formData.append('original', rawImages.value.before);
      if (algorithm === 'alpha') {
      formData.append('reference', rawImages.value.reference);
      }
      formData.append('student', rawImages.value.after);

      const url = `http://localhost:3000/api/algorithms/${algorithm}/compare`;
      console.log('Enviando para', url, 'FormData keys:', [...formData.keys()]);

      try {
        const response = await fetch(url, { method: 'POST', body: formData });
        const data = await response.json();
        if (response.ok) {
          result.value = data;
        } else {
          alert(data.message || 'Erro ao processar as imagens.');
        }
      } catch (err) {
        console.error('Erro de conexão:', err);
        alert('Erro de conexão com o servidor.');
      }
    };

    /* ---- realce de sintaxe do código fonte ---- */
    const highlightedCode = computed(() => {
      if (!result.value?.sourceCode) return '';
      return Prism.highlight(
        result.value.sourceCode,
        Prism.languages.python,
        'python'
      );
    });

    /* ---- expõe para o template ---- */
    return {
      authState,
      rawImages,
      imageNames,
      preview,
      result,
      highlightedCode,
      handleImageUpload,
      submitImages,
      algorithmCategories,
      expanded,
    };
  },
};
</script>

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 100vh;
}

.main-content {
  text-align: center;
  padding: 50px 20px;
  flex: 1;
}

.image-uploader {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.custom-file-upload {
  display: inline-block;
  padding: 10px 20px;
  font-size: 16px;
  font-weight: bold;
  color: white;
  background-color: #333;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

.custom-file-upload:hover {
  background-color: #555;
  transform: scale(1.05);
}

.custom-file-upload input[type='file'] {
  display: none;
}

.preview-img {
  max-width: 250px;
  max-height: 200px;
  margin-top: 8px;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  object-fit: contain;
}

.algorithms-container {
  margin-top: 20px;
  width: 100%;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.category-section {
  margin-bottom: 10px;
  border: 1px solid #444;
  border-radius: 8px;
  overflow: hidden;
  background-color: #f5f5f5;
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #333;
  color: white;
  padding: 12px 16px;
  font-weight: 600;
  cursor: pointer;
  user-select: none;
}

.category-header:hover {
  background-color: #444;
}

.toggle-icon {
  font-size: 14px;
}

.category-items {
  display: flex;
  flex-direction: column;
  padding: 10px;
  gap: 8px;
  background-color: #eee;
}

.alg-button {
  background-color: #333;
  color: white;
  border: none;
  padding: 10px 12px;
  border-radius: 6px;
  cursor: pointer;
  text-align: center;
  transition: background-color 0.2s;
}

.alg-button:hover {
  background-color: #555;
}

.alg-button:active {
  transform: scale(0.98);
}

.result-box {
  margin-top: 20px;
}

.success {
  color: green;
  font-weight: 600;
  margin-top: 5px;
}

.error {
  color: #c00;
  font-weight: 600;
  margin-top: 5px;
}

.code-block {
  max-width: 900px;
  width: 90%;
  margin: 14px auto;
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
  font-family: 'Fira Code', 'Consolas', monospace;
  line-height: 1.4;
}

.code-block code {
  white-space: pre;
  tab-size: 4;
  -moz-tab-size: 4;
  display: block;
  text-align: left;
}

</style>
