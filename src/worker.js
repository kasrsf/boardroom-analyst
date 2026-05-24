export default {
  async fetch(request, env) {
    const response = await env.ASSETS.fetch(request);
    if (response.status !== 404) {
      return response;
    }

    const requestUrl = new URL(request.url);
    requestUrl.pathname = "/404.html";

    const notFound = await env.ASSETS.fetch(new Request(requestUrl, request));
    return new Response(notFound.body, {
      status: 404,
      headers: notFound.headers
    });
  }
};
