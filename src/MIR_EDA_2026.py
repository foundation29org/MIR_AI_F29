"""
Script para análisis exploratorio de datos (EDA) del MIR 2026.
Genera gráficas de precisión por especialidad para cada modelo.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Mapeo de abreviaturas a nombres completos de especialidades
SPECIALTY_MAP = {
    # Especialidades médicas principales
    'CD': 'Cardiología',
    'CD (CV)': 'Cardiología',
    'CD(CV)': 'Cardiología',
    'DG': 'Digestivo',
    'NR': 'Neurología',
    'NR (NQ)': 'Neurología',
    'NM': 'Neumología',
    'NM (CT)': 'Neumología',
    'DM': 'Dermatología',
    'IF': 'Infecciosas',
    'HM': 'Hematología',
    'NF': 'Nefrología',
    'ED': 'Endocrinología',
    'PQ': 'Psiquiatría',
    'PQ ': 'Psiquiatría',
    'TM': 'Traumatología',
    'RH': 'Reumatología',
    'GC': 'Ginecología',
    'GR': 'Ginecología',
    'GT': 'Genética',
    'PD': 'Pediatría',
    'PD 2.1': 'Pediatría',
    'PD 4.11': 'Pediatría',
    'UR': 'Urología',
    'UG': 'Urgencias',
    'OF': 'Oftalmología',
    'OR': 'ORL',
    'OR (CM)': 'ORL',
    'ORL': 'ORL',
    'ON': 'Oncología',
    'CG': 'Cirugía General',
    'CG (CP)': 'Cirugía General',
    'AL': 'Alergología',
    'IG': 'Inmunología',
    
    # Básicas y transversales
    'EP': 'Epidemiología',
    'BE': 'Bioética',
    'FC': 'Farmacología',
    'FM': 'Medicina Familiar',
    'FS': 'Fisiología',
    'AN': 'Anatomía',
    'AP': 'Anatomía Patológica',
    'BQ': 'Bioquímica',
    'BQ/PD': 'Bioquímica',
    'AT': 'Anestesiología',
    'RM': 'Rehabilitación',
    'RX': 'Radiología',
    'DR': 'Radiología',
}

def load_data():
    """Carga y combina los datos del Excel oficial con los resultados de los modelos."""
    
    # Cargar Excel oficial con especialidades
    oficial_path = 'data/Excel MIR 2026.xlsx'
    df_oficial = pd.read_excel(oficial_path)
    
    # Cargar resultados de modelos
    results_path = 'data/MIR26.xlsx'
    df_results = pd.read_excel(results_path)
    
    print(f"Excel oficial: {len(df_oficial)} filas")
    print(f"Resultados modelos: {len(df_results)} filas")
    print(f"Columnas oficiales: {df_oficial.columns.tolist()}")
    print(f"Columnas resultados: {df_results.columns.tolist()}")
    
    # Mapear especialidad principal (ASIGNATURA 1)
    df_oficial['Especialidad'] = df_oficial['ASIGNATURA 1'].map(SPECIALTY_MAP)
    
    # Rellenar valores no mapeados
    unmapped = df_oficial[df_oficial['Especialidad'].isna()]['ASIGNATURA 1'].unique()
    if len(unmapped) > 0:
        print(f"\nAbreviaturas no mapeadas: {unmapped}")
        # Usar la abreviatura original si no hay mapeo
        df_oficial['Especialidad'] = df_oficial['Especialidad'].fillna(df_oficial['ASIGNATURA 1'])
    
    # Combinar por número de pregunta
    df_merged = df_results.merge(
        df_oficial[['PREGUNTA', 'RESPUESTA', 'Especialidad', 'ASIGNATURA 1']],
        left_on='qnum',
        right_on='PREGUNTA',
        how='left'
    )
    
    # Normalizar respuesta correcta (convertir 1.0 -> "1")
    df_merged['correct_answer'] = df_merged['RESPUESTA'].apply(
        lambda x: str(int(x)) if pd.notna(x) and str(x).replace('.0', '').isdigit() else str(x)
    )
    
    return df_merged

def get_answer_columns(df):
    """Obtiene las columnas de respuestas de modelos."""
    return [col for col in df.columns if col.startswith('answer_')]

def calculate_accuracy_by_specialty(df, answer_col):
    """Calcula la precisión por especialidad para un modelo."""
    results = []
    
    for specialty in df['Especialidad'].dropna().unique():
        subset = df[df['Especialidad'] == specialty]
        
        # Filtrar filas con respuestas válidas
        valid = subset[
            (subset[answer_col].notna()) & 
            (subset[answer_col].astype(str) != 'ERROR') &
            (subset[answer_col].astype(str) != '') &
            (subset[answer_col].astype(str) != 'nan')
        ]
        
        if len(valid) > 0:
            # Convertir a string y comparar solo el primer carácter numérico
            model_answers = valid[answer_col].astype(str).str.strip()
            correct_answers = valid['correct_answer'].astype(str).str.strip()
            
            correct = (model_answers == correct_answers).sum()
            total = len(valid)
            accuracy = correct / total * 100
            results.append({
                'Especialidad': specialty,
                'Aciertos': int(correct),
                'Total': int(total),
                'Precisión': accuracy
            })
    
    return pd.DataFrame(results)

def plot_accuracy_by_specialty(df, model_name, output_dir='results/charts'):
    """Genera gráfica de precisión por especialidad para un modelo."""
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Ordenar por precisión descendente
    df_sorted = df.sort_values('Precisión', ascending=True)
    
    # Crear paleta de colores
    colors = sns.color_palette('rocket_r', len(df_sorted))
    
    fig, ax = plt.subplots(figsize=(12, 10), dpi=150)
    
    bars = ax.barh(df_sorted['Especialidad'], df_sorted['Precisión'], color=colors)
    
    # Añadir etiquetas con porcentaje
    for bar, (_, row) in zip(bars, df_sorted.iterrows()):
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2, 
                f'{row["Precisión"]:.1f}% ({row["Aciertos"]}/{row["Total"]})',
                va='center', fontsize=9)
    
    ax.set_xlabel('Precisión (%)')
    ax.set_title(f'Precisión de {model_name} por Especialidad (MIR 2026)')
    ax.set_xlim(0, 110)
    
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, f'{model_name}_by_specialty.png')
    fig.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Gráfica guardada: {output_path}")
    
    return output_path

def plot_all_models_comparison(all_results, output_dir='results/charts'):
    """Genera gráfica comparativa de todos los modelos."""
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Crear DataFrame con precisión global por modelo
    summary = []
    for model_name, df in all_results.items():
        total_correct = df['Aciertos'].sum()
        total_questions = df['Total'].sum()
        accuracy = total_correct / total_questions * 100
        summary.append({
            'Modelo': model_name,
            'Precisión': accuracy,
            'Aciertos': total_correct,
            'Total': total_questions
        })
    
    df_summary = pd.DataFrame(summary).sort_values('Precisión', ascending=True)
    
    # Crear gráfica
    colors = sns.color_palette('viridis', len(df_summary))
    
    fig, ax = plt.subplots(figsize=(10, 8), dpi=150)
    
    bars = ax.barh(df_summary['Modelo'], df_summary['Precisión'], color=colors)
    
    for bar, (_, row) in zip(bars, df_summary.iterrows()):
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2, 
                f'{row["Precisión"]:.1f}%',
                va='center', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('Precisión (%)')
    ax.set_title('Comparación de Modelos - MIR 2026')
    ax.set_xlim(0, 105)
    
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, 'models_comparison.png')
    fig.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Gráfica comparativa guardada: {output_path}")
    
    return output_path

def plot_image_vs_text_comparison(df, answer_cols, output_dir='results/charts'):
    """Genera gráfica comparativa de rendimiento con/sin imagen."""
    
    os.makedirs(output_dir, exist_ok=True)
    
    results = []
    for col in answer_cols:
        model_name = col.replace('answer_', '')
        
        # Con imagen
        with_img = df[df['image_refs'].notna() & (df['image_refs'] != '')]
        valid_img = with_img[
            (with_img[col].notna()) & 
            (with_img[col].astype(str) != 'ERROR') &
            (with_img[col].astype(str) != 'nan')
        ]
        if len(valid_img) > 0:
            acc_img = (valid_img[col].astype(str).str.strip() == valid_img['correct_answer'].astype(str).str.strip()).mean() * 100
        else:
            acc_img = 0
        
        # Sin imagen
        no_img = df[df['image_refs'].isna() | (df['image_refs'] == '')]
        valid_no_img = no_img[
            (no_img[col].notna()) & 
            (no_img[col].astype(str) != 'ERROR') &
            (no_img[col].astype(str) != 'nan')
        ]
        if len(valid_no_img) > 0:
            acc_no_img = (valid_no_img[col].astype(str).str.strip() == valid_no_img['correct_answer'].astype(str).str.strip()).mean() * 100
        else:
            acc_no_img = 0
        
        results.append({
            'Modelo': model_name,
            'Con Imagen': acc_img,
            'Sin Imagen': acc_no_img
        })
    
    df_results = pd.DataFrame(results)
    df_results = df_results.sort_values('Sin Imagen', ascending=True)
    
    # Crear gráfica de barras agrupadas
    fig, ax = plt.subplots(figsize=(12, 8), dpi=150)
    
    x = range(len(df_results))
    width = 0.35
    
    bars1 = ax.barh([i - width/2 for i in x], df_results['Con Imagen'], width, 
                    label='Con Imagen', color='#e74c3c', alpha=0.8)
    bars2 = ax.barh([i + width/2 for i in x], df_results['Sin Imagen'], width, 
                    label='Sin Imagen', color='#3498db', alpha=0.8)
    
    ax.set_yticks(x)
    ax.set_yticklabels(df_results['Modelo'])
    ax.set_xlabel('Precisión (%)')
    ax.set_title('Rendimiento por Tipo de Pregunta - MIR 2026')
    ax.legend(loc='lower right')
    ax.set_xlim(0, 105)
    
    # Añadir valores
    for bar in bars1:
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2, f'{width:.1f}%',
                va='center', fontsize=8, color='#c0392b')
    for bar in bars2:
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2, f'{width:.1f}%',
                va='center', fontsize=8, color='#2980b9')
    
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, 'image_vs_text_comparison.png')
    fig.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Gráfica con/sin imagen guardada: {output_path}")
    return output_path


def plot_model_correlation_heatmap(df, answer_cols, output_dir='results/charts'):
    """Genera heatmap de correlación/concordancia entre modelos."""
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Crear matriz de concordancia
    model_names = [col.replace('answer_', '') for col in answer_cols]
    n_models = len(model_names)
    concordance = pd.DataFrame(index=model_names, columns=model_names, dtype=float)
    
    for i, col1 in enumerate(answer_cols):
        for j, col2 in enumerate(answer_cols):
            # Filtrar filas válidas para ambos modelos
            valid = df[
                (df[col1].notna()) & (df[col1].astype(str) != 'ERROR') &
                (df[col2].notna()) & (df[col2].astype(str) != 'ERROR')
            ]
            if len(valid) > 0:
                matches = (valid[col1].astype(str).str.strip() == valid[col2].astype(str).str.strip()).mean()
                concordance.iloc[i, j] = matches
            else:
                concordance.iloc[i, j] = 0
    
    concordance = concordance.astype(float)
    
    # Crear heatmap
    fig, ax = plt.subplots(figsize=(10, 8), dpi=150)
    
    sns.heatmap(concordance, annot=True, fmt='.2f', cmap='RdYlGn', 
                vmin=0.5, vmax=1.0, ax=ax, 
                linewidths=0.5, linecolor='white',
                cbar_kws={'label': 'Concordancia'})
    
    ax.set_title('Concordancia entre Modelos - MIR 2026\n(Proporción de respuestas iguales)')
    
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, 'model_concordance_heatmap.png')
    fig.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Heatmap de concordancia guardado: {output_path}")
    return output_path


def plot_specialty_distribution(df, output_dir='results/charts'):
    """Genera gráfica de distribución de preguntas por especialidad."""
    
    os.makedirs(output_dir, exist_ok=True)
    
    specialty_counts = df['Especialidad'].value_counts()
    
    fig, ax = plt.subplots(figsize=(12, 8), dpi=150)
    
    colors = sns.color_palette('husl', len(specialty_counts))
    bars = ax.barh(specialty_counts.index[::-1], specialty_counts.values[::-1], color=colors[::-1])
    
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.3, bar.get_y() + bar.get_height()/2, f'{int(width)}',
                va='center', fontsize=9)
    
    ax.set_xlabel('Número de Preguntas')
    ax.set_title('Distribución de Preguntas por Especialidad - MIR 2026')
    
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, 'specialty_distribution.png')
    fig.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Distribución por especialidad guardada: {output_path}")
    return output_path


def main():
    print("="*60)
    print("MIR 2026 - Análisis por Especialidad")
    print("="*60)
    
    # Cargar datos
    df = load_data()
    
    print(f"\nEspecialidades encontradas: {df['Especialidad'].nunique()}")
    print(df['Especialidad'].value_counts())
    
    # Obtener columnas de modelos
    answer_cols = get_answer_columns(df)
    print(f"\nModelos encontrados: {[col.replace('answer_', '') for col in answer_cols]}")
    
    if len(answer_cols) == 0:
        print("No se encontraron columnas de respuestas de modelos.")
        return
    
    # Calcular precisión por especialidad para cada modelo
    all_results = {}
    
    for col in answer_cols:
        model_name = col.replace('answer_', '')
        print(f"\nProcesando {model_name}...")
        
        accuracy_df = calculate_accuracy_by_specialty(df, col)
        
        if len(accuracy_df) > 0:
            all_results[model_name] = accuracy_df
            
            # Generar gráfica individual
            plot_accuracy_by_specialty(accuracy_df, model_name)
            
            # Mostrar resumen
            print(f"  Especialidades: {len(accuracy_df)}")
            print(f"  Mejor: {accuracy_df.loc[accuracy_df['Precisión'].idxmax(), 'Especialidad']} ({accuracy_df['Precisión'].max():.1f}%)")
            print(f"  Peor: {accuracy_df.loc[accuracy_df['Precisión'].idxmin(), 'Especialidad']} ({accuracy_df['Precisión'].min():.1f}%)")
    
    # Gráfica comparativa
    if len(all_results) > 1:
        plot_all_models_comparison(all_results)
    
    # Gráficas adicionales
    print("\nGenerando gráficas adicionales...")
    plot_image_vs_text_comparison(df, answer_cols)
    plot_model_correlation_heatmap(df, answer_cols)
    plot_specialty_distribution(df)
    
    print("\n" + "="*60)
    print("Análisis completado. Gráficas guardadas en results/charts/")
    print("="*60)

if __name__ == '__main__':
    main()
