async def get_video_url(data):
    if data['success']:
        if 'links' in data:
            if isinstance(data['links'], list):
                video_url = next((link['link'] for link in data['links'] if link['quality']
                                 == 'video_hd_original' or link['quality'] == 'video_hd_original_0'), None)
                if not video_url:
                    video_url = next(
                        (link['link'] for link in data['links'] if 'video' in link['quality'].lower()), None)
                return video_url
    return None
