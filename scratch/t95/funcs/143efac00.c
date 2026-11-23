char __fastcall sub_143EFAC00(__int64 a1)
{
  __int64 v1; // rdx
  char v2; // al
  _BYTE *v3; // rcx
  _BYTE *v4; // rdx
  char result; // al

  if ( (_BYTE)word_141B60320 == 0 )
    return 0;
  v1 = *(_QWORD *)(*(_QWORD *)(a1 + 368) + 288LL);
  if ( v1 == 0 )
    return 0;
  v2 = *(_BYTE *)(a1 + 185);
  if ( v2 != 0 )
  {
    v3 = *(_BYTE **)(v1 + 624);
    if ( v3 == nullptr )
      return 0;
  }
  else
  {
    v3 = *(_BYTE **)(v1 + 624);
  }
  v4 = (_BYTE *)(v1 + 88);
  if ( v2 != 0 )
    v4 = v3;
  if ( v4 == nullptr )
    return 0;
  if ( *(_BYTE *)(*(_QWORD *)v4 + 68LL) == 0 )
    return 0;
  result = 1;
  if ( v4[522] == 3 )
    return 0;
  return result;
}
