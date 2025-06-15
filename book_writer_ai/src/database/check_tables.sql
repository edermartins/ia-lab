-- Verificar se a tabela chapters existe
SELECT EXISTS (
    SELECT FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name = 'chapters'
);

-- Verificar a estrutura da tabela chapters
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
AND table_name = 'chapters'
ORDER BY ordinal_position;

-- Verificar se existem registros na tabela chapters
SELECT COUNT(*) FROM chapters;

-- Verificar os registros da tabela chapters
SELECT * FROM chapters; 