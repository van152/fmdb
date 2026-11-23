char __fastcall sub_143862E80(__int64 a1)
{
  int v1; // ecx
  char result; // al
  int v3; // edx
  unsigned __int64 v4; // rcx
  __int64 v5; // rdx

  v1 = *(_DWORD *)(a1 + 12);
  result = 1;
  if ( v1 > 1803481 )
  {
    if ( v1 > 23341951 )
    {
      if ( v1 > 66029611 )
      {
        if ( (unsigned int)(v1 - 66029612) < 2 || v1 == 72005153 || v1 == 2000004793 )
          return result;
      }
      else if ( v1 <= 31037813 )
      {
        if ( v1 == 23341952 || v1 == 23348937 )
          return result;
      }
      else if ( v1 == 31037814 || v1 == 45015071 || v1 == 45015548 )
      {
        return result;
      }
    }
    else if ( v1 > 5628783 )
    {
      if ( (unsigned int)(v1 - 23043716) < 2 || v1 == 5628784 || v1 == 23071816 )
        return result;
    }
    else if ( (unsigned int)(v1 - 1803482) < 2 || (unsigned int)(v1 - 5628523) < 2 || v1 == 4400013 )
    {
      return result;
    }
    return 0;
  }
  if ( v1 > 562394 )
  {
    if ( (unsigned int)(v1 - 562395) < 4 || (unsigned int)(v1 - 786445) < 2 || v1 == 981732 )
      return result;
    return 0;
  }
  if ( v1 <= 215304 )
  {
    if ( (unsigned int)(v1 - 109132) < 2 || v1 == 130834 || v1 == 136549 )
      return result;
    return 0;
  }
  if ( (unsigned int)(v1 - 225496) > 0x12 || (v3 = 266305, !_bittest(&v3, v1 - 225496)) )
  {
    v4 = (unsigned int)(v1 - 215305);
    if ( (unsigned int)v4 > 0x36 )
      return 0;
    v5 = 0x40000000000003LL;
    if ( !_bittest64(&v5, v4) )
      return 0;
  }
  return result;
}
