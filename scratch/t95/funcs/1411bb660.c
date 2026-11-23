// THUNK ALIAS -> sub_143FF8D90 (jmp:0x1411bb660->0x143ff8d90)
char __fastcall sub_143FF8D90(__int64 a1)
{
  int v2; // ecx
  char result; // al
  unsigned __int64 v4; // rcx
  __int64 v5; // rdx

  if ( (unsigned __int8)sub_140087070() == 0 )
    return 0;
  v2 = *(_DWORD *)(a1 + 12);
  result = 1;
  if ( v2 > 72023744 )
  {
    if ( v2 > 72047535 )
    {
      if ( v2 > 90086692 )
      {
        if ( (unsigned int)(v2 - 2000034550) < 2 || v2 == 90086693 || v2 == 2000153734 )
          return result;
      }
      else if ( v2 == 72047536 || v2 == 72049317 || v2 == 72053495 )
      {
        return result;
      }
    }
    else if ( v2 <= 72037351 )
    {
      v4 = (unsigned int)(v2 - 72023745);
      if ( (unsigned int)v4 <= 0x31 )
      {
        v5 = 0x2000000000009LL;
        if ( _bittest64(&v5, v4) )
          return result;
      }
    }
    else if ( v2 > 72042355 )
    {
      if ( v2 == 72042356 || v2 == 72042360 )
        return result;
    }
    else if ( v2 == 72037352 || v2 == 72037354 )
    {
      return result;
    }
    return 0;
  }
  if ( ((unsigned int)(v2 - 72006961) > 0xD || v2 == 72006969) && v2 != 164040 && v2 != 31051842 )
    return 0;
  return result;
}
