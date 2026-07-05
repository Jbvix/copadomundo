/**
 * Proxy serverless para a pesquisa de satisfação (Supabase).
 * - POST: qualquer visitante pode enviar feedback (nota de 1 a 5 + comentário opcional).
 *   Aplica um guardrail de linguagem no comentário antes de gravar.
 * - GET: só retorna as respostas se o header "x-admin-password" bater com a variável de
 *   ambiente ADMIN_PASSWORD — usado pelo painel admin acessível pela splash screen.
 * - Mantém a chave do Supabase exclusivamente no servidor (nunca exposta ao cliente).
 *
 * Variáveis de ambiente exigidas no painel do Netlify:
 *   SUPABASE_URL, SUPABASE_ANON_KEY, ADMIN_PASSWORD
 */

const SUPABASE_URL = process.env.SUPABASE_URL || '';
const SUPABASE_KEY = process.env.SUPABASE_ANON_KEY || '';
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || '';

// Guardrail simples de linguagem (mesmo espírito do filtro do Téo no front-end),
// repetido aqui porque o comentário tem que ser validado no servidor, não só no navegador.
const TERMOS_IMPROPRIOS = [
    /\b(porra|caralho|merda|puta|fdp|vsf|vai tomar|filho da|desgraçad|babaca|idiota|imbecil|retardad|macaco|hitler|nazi)\b/i,
    /\b(fuck|shit|bitch|asshole|nigger|faggot)\b/i,
];

function contemTermoImproprio(texto) {
    return TERMOS_IMPROPRIOS.some((rx) => rx.test(String(texto || '')));
}

exports.handler = async function (event) {
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, x-admin-password',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Content-Type': 'application/json',
    };

    if (event.httpMethod === 'OPTIONS') {
        return { statusCode: 200, headers, body: '' };
    }

    if (!SUPABASE_URL || !SUPABASE_KEY) {
        console.error('ERRO: SUPABASE_URL/SUPABASE_ANON_KEY não configuradas.');
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ error: 'Backend de feedback não configurado no servidor.' }),
        };
    }

    if (event.httpMethod === 'POST') return handlePost(event, headers);
    if (event.httpMethod === 'GET') return handleGet(event, headers);

    return {
        statusCode: 405,
        headers,
        body: JSON.stringify({ error: 'Método Não Permitido. Utilize GET ou POST.' }),
    };
};

async function handlePost(event, headers) {
    let body;
    try {
        body = JSON.parse(event.body || '{}');
    } catch (e) {
        return { statusCode: 400, headers, body: JSON.stringify({ error: 'JSON inválido no corpo da requisição.' }) };
    }

    const rating = Number(body.rating);
    if (!Number.isInteger(rating) || rating < 1 || rating > 5) {
        return { statusCode: 400, headers, body: JSON.stringify({ error: 'Nota inválida (esperado um inteiro de 1 a 5).' }) };
    }

    let comentario = typeof body.comentario === 'string' ? body.comentario.trim().slice(0, 500) : null;
    if (comentario === '') comentario = null;

    if (comentario && contemTermoImproprio(comentario)) {
        return {
            statusCode: 400,
            headers,
            body: JSON.stringify({ error: 'Comentário com linguagem imprópria. Reformule com respeito, por favor.' }),
        };
    }

    try {
        const resp = await fetch(`${SUPABASE_URL}/rest/v1/feedback`, {
            method: 'POST',
            headers: {
                apikey: SUPABASE_KEY,
                Authorization: `Bearer ${SUPABASE_KEY}`,
                'Content-Type': 'application/json',
                Prefer: 'return=minimal',
            },
            body: JSON.stringify({ rating, comentario }),
        });

        if (!resp.ok) {
            const text = await resp.text();
            console.error('Erro ao gravar feedback no Supabase:', resp.status, text);
            return { statusCode: 502, headers, body: JSON.stringify({ error: 'Falha ao salvar o feedback.' }) };
        }

        return { statusCode: 201, headers, body: JSON.stringify({ ok: true }) };
    } catch (err) {
        console.error('Falha de rede ao gravar feedback:', err);
        return { statusCode: 500, headers, body: JSON.stringify({ error: 'Falha interna ao salvar o feedback.' }) };
    }
}

async function handleGet(event, headers) {
    const senhaEnviada = (event.headers && (event.headers['x-admin-password'] || event.headers['X-Admin-Password'])) || '';

    if (!ADMIN_PASSWORD) {
        console.error('ERRO: ADMIN_PASSWORD não configurada — acesso admin desativado.');
        return { statusCode: 500, headers, body: JSON.stringify({ error: 'Acesso admin não configurado no servidor.' }) };
    }
    if (senhaEnviada !== ADMIN_PASSWORD) {
        return { statusCode: 401, headers, body: JSON.stringify({ error: 'Senha de admin inválida.' }) };
    }

    try {
        const resp = await fetch(
            `${SUPABASE_URL}/rest/v1/feedback?select=id,rating,comentario,criado_em&order=criado_em.desc&limit=500`,
            {
                method: 'GET',
                headers: {
                    apikey: SUPABASE_KEY,
                    Authorization: `Bearer ${SUPABASE_KEY}`,
                },
            }
        );

        if (!resp.ok) {
            const text = await resp.text();
            console.error('Erro ao ler feedback do Supabase:', resp.status, text);
            return { statusCode: 502, headers, body: JSON.stringify({ error: 'Falha ao carregar as respostas.' }) };
        }

        const respostas = await resp.json();
        return { statusCode: 200, headers, body: JSON.stringify({ respostas }) };
    } catch (err) {
        console.error('Falha de rede ao ler feedback:', err);
        return { statusCode: 500, headers, body: JSON.stringify({ error: 'Falha interna ao carregar as respostas.' }) };
    }
}
