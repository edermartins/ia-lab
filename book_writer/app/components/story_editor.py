import streamlit as st
from typing import Dict, List
import json
from utils.llm_interface import LLMInterface

class StoryEditor:
    def __init__(self, llm_interface: LLMInterface):
        self.llm = llm_interface
        
        # Carregar dados da história
        if "story" not in st.session_state:
            st.session_state.story = {
                "title": "",
                "genre": "",
                "synopsis": "",
                "chapters": [],
                "timeline": []
            }
    
    def render(self):
        st.header("Editor de História")
        
        # Sidebar para navegação
        with st.sidebar:
            st.subheader("Navegação")
            page = st.radio(
                "Selecione uma seção:",
                ["Visão Geral", "Capítulos", "Linha do Tempo", "Revisão"]
            )
        
        # Renderizar a seção selecionada
        if page == "Visão Geral":
            self._render_overview()
        elif page == "Capítulos":
            self._render_chapters()
        elif page == "Linha do Tempo":
            self._render_timeline()
        elif page == "Revisão":
            self._render_review()
    
    def _render_overview(self):
        st.subheader("Visão Geral da História")
        
        # Informações básicas
        title = st.text_input("Título do Livro", value=st.session_state.story["title"])
        genre = st.selectbox(
            "Gênero",
            ["Ficção", "Fantasia", "Ficção Científica", "Romance", "Mistério", "Aventura"],
            index=0 if not st.session_state.story["genre"] else ["Ficção", "Fantasia", "Ficção Científica", "Romance", "Mistério", "Aventura"].index(st.session_state.story["genre"])
        )
        
        # Sinopse
        st.subheader("Sinopse")
        synopsis = st.text_area(
            "Sinopse da História",
            value=st.session_state.story["synopsis"],
            height=200
        )
        
        # Botões de ação
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Salvar Informações"):
                self._save_story_info({
                    "title": title,
                    "genre": genre,
                    "synopsis": synopsis
                })
        
        with col2:
            if st.button("Gerar Sinopse com IA"):
                self._generate_synopsis(title, genre)
        
        # Estatísticas
        st.subheader("Estatísticas")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Capítulos", len(st.session_state.story["chapters"]))
        with col2:
            st.metric("Personagens", len(st.session_state.get("characters", {})))
        with col3:
            st.metric("Ambientes", len(st.session_state.get("environments", {})))
    
    def _render_chapters(self):
        st.subheader("Capítulos")
        
        # Lista de capítulos
        for i, chapter in enumerate(st.session_state.story["chapters"]):
            with st.expander(f"Capítulo {i+1}: {chapter['title']}"):
                # Editar capítulo
                title = st.text_input("Título", value=chapter["title"], key=f"chapter_title_{i}")
                content = st.text_area("Conteúdo", value=chapter["content"], height=200, key=f"chapter_content_{i}")
                
                # Personagens no capítulo
                st.subheader("Personagens Presentes")
                characters = st.multiselect(
                    "Selecione os personagens",
                    options=list(st.session_state.get("characters", {}).keys()),
                    default=chapter.get("characters", []),
                    key=f"chapter_characters_{i}"
                )
                
                # Ambientes do capítulo
                st.subheader("Ambientes do Capítulo")
                environments = st.multiselect(
                    "Selecione os ambientes",
                    options=list(st.session_state.get("environments", {}).keys()),
                    default=chapter.get("environments", []),
                    key=f"chapter_environments_{i}"
                )
                
                # Botões de ação
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Salvar Capítulo", key=f"save_chapter_{i}"):
                        self._save_chapter(i, {
                            "title": title,
                            "content": content,
                            "characters": characters,
                            "environments": environments
                        })
                
                with col2:
                    if st.button("Gerar com IA", key=f"generate_chapter_{i}"):
                        self._generate_chapter_content(i, title, characters, environments)
        
        # Adicionar novo capítulo
        if st.button("Adicionar Novo Capítulo"):
            st.session_state.story["chapters"].append({
                "title": f"Capítulo {len(st.session_state.story['chapters']) + 1}",
                "content": "",
                "characters": [],
                "environments": []
            })
            st.experimental_rerun()
    
    def _render_timeline(self):
        st.subheader("Linha do Tempo")
        
        # Visualização da linha do tempo
        for i, event in enumerate(st.session_state.story["timeline"]):
            with st.expander(f"Evento {i+1}: {event['title']}"):
                # Editar evento
                title = st.text_input("Título do Evento", value=event["title"], key=f"event_title_{i}")
                description = st.text_area("Descrição", value=event["description"], height=100, key=f"event_description_{i}")
                chapter = st.number_input("Capítulo", value=event["chapter"], min_value=1, key=f"event_chapter_{i}")
                
                # Botões de ação
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Salvar Evento", key=f"save_event_{i}"):
                        self._save_timeline_event(i, {
                            "title": title,
                            "description": description,
                            "chapter": chapter
                        })
                
                with col2:
                    if st.button("Remover Evento", key=f"remove_event_{i}"):
                        self._remove_timeline_event(i)
        
        # Adicionar novo evento
        if st.button("Adicionar Novo Evento"):
            st.session_state.story["timeline"].append({
                "title": f"Evento {len(st.session_state.story['timeline']) + 1}",
                "description": "",
                "chapter": 1
            })
            st.experimental_rerun()
    
    def _render_review(self):
        st.subheader("Revisão e Coerência")
        
        # Análise de coerência
        if st.button("Analisar Coerência"):
            self._analyze_coherence()
        
        # Sugestões de melhoria
        if "coherence_analysis" in st.session_state:
            st.subheader("Análise de Coerência")
            st.write(st.session_state.coherence_analysis)
            
            # Sugestões específicas
            if "suggestions" in st.session_state.coherence_analysis:
                st.subheader("Sugestões de Melhoria")
                for suggestion in st.session_state.coherence_analysis["suggestions"]:
                    st.write(f"- {suggestion}")
    
    def _save_story_info(self, info: Dict):
        """Salva as informações básicas da história."""
        st.session_state.story.update(info)
        st.success("Informações salvas com sucesso!")
    
    def _save_chapter(self, index: int, chapter_data: Dict):
        """Salva os dados de um capítulo."""
        st.session_state.story["chapters"][index] = chapter_data
        st.success("Capítulo salvo com sucesso!")
    
    def _save_timeline_event(self, index: int, event_data: Dict):
        """Salva um evento na linha do tempo."""
        st.session_state.story["timeline"][index] = event_data
        st.success("Evento salvo com sucesso!")
    
    def _remove_timeline_event(self, index: int):
        """Remove um evento da linha do tempo."""
        st.session_state.story["timeline"].pop(index)
        st.success("Evento removido com sucesso!")
        st.experimental_rerun()
    
    def _generate_synopsis(self, title: str, genre: str):
        """Gera uma sinopse usando IA."""
        if not title:
            st.warning("Por favor, insira um título para a história.")
            return
        
        prompt = f"""
        Crie uma sinopse envolvente para um livro com as seguintes informações:
        Título: {title}
        Gênero: {genre}
        
        A sinopse deve ser concisa mas informativa, despertando interesse no leitor.
        """
        
        response = self.llm.generate_response(prompt)
        st.session_state.story["synopsis"] = response
        st.success("Sinopse gerada com sucesso!")
    
    def _generate_chapter_content(self, chapter_index: int, title: str, characters: List[str], environments: List[str]):
        """Gera o conteúdo de um capítulo usando IA."""
        if not title:
            st.warning("Por favor, insira um título para o capítulo.")
            return
        
        # Obter informações dos personagens e ambientes
        character_info = [st.session_state.characters[char] for char in characters if char in st.session_state.characters]
        environment_info = [st.session_state.environments[env] for env in environments if env in st.session_state.environments]
        
        prompt = f"""
        Crie o conteúdo para um capítulo de livro com as seguintes informações:
        Título do Capítulo: {title}
        
        Personagens presentes:
        {json.dumps(character_info, indent=2)}
        
        Ambientes:
        {json.dumps(environment_info, indent=2)}
        
        Por favor, crie um capítulo envolvente que desenvolva a história e os personagens.
        """
        
        response = self.llm.generate_response(prompt)
        st.session_state.story["chapters"][chapter_index]["content"] = response
        st.success("Conteúdo do capítulo gerado com sucesso!")
    
    def _analyze_coherence(self):
        """Analisa a coerência da história."""
        story_data = {
            "title": st.session_state.story["title"],
            "genre": st.session_state.story["genre"],
            "synopsis": st.session_state.story["synopsis"],
            "chapters": st.session_state.story["chapters"],
            "timeline": st.session_state.story["timeline"],
            "characters": st.session_state.get("characters", {}),
            "environments": st.session_state.get("environments", {})
        }
        
        prompt = f"""
        Analise a coerência da seguinte história e forneça sugestões de melhoria:
        {json.dumps(story_data, indent=2)}
        
        Verifique:
        1. Consistência da trama
        2. Desenvolvimento dos personagens
        3. Uso dos ambientes
        4. Continuidade da linha do tempo
        5. Coerência com o gênero
        
        Formate a resposta em JSON com as chaves: analysis, suggestions
        """
        
        response = self.llm.generate_response(prompt)
        try:
            analysis = json.loads(response)
            st.session_state.coherence_analysis = analysis
            st.success("Análise de coerência concluída!")
        except json.JSONDecodeError:
            st.error("Erro ao processar a análise de coerência") 