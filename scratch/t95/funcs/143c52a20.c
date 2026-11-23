__int64 __fastcall sub_143C52A20(__int64 a1, char a2)
{
  __int64 **v3; // rsi
  char **v4; // rcx
  char **v5; // rax
  __int64 v6; // rdi
  int v7; // r8d
  __int64 *v8; // rax
  unsigned int v9; // edi

  if ( (_BYTE)word_141B60320 == 0 )
    return a1;
  v3 = *(__int64 ***)(a1 + 280);
  v4 = *(char ***)(a1 + 288);
  if ( v3 == (__int64 **)v4 )
    return a1;
  v5 = *(char ***)(a1 + 280);
  while ( 1 )
  {
    if ( (*v5)[30] < 0 )
    {
      v6 = *(_QWORD *)*v5;
      if ( v6 != a1 )
        break;
    }
    if ( ++v5 == v4 )
      goto LABEL_8;
  }
  if ( v6 != 0 )
    return v6;
LABEL_8:
  v7 = 1049072;
  while ( 1 )
  {
    v8 = *v3;
    if ( (*v3)[1] == a1 )
    {
      v9 = *((unsigned __int8 *)v8 + 48);
      if ( v9 <= 0x14 )
      {
        if ( _bittest(&v7, v9) )
          break;
      }
    }
    if ( ++v3 == (__int64 **)v4 )
      return a1;
  }
  v6 = *v8;
  if ( *v8 == 0 || (*(_BYTE *)(v6 + 352) & 4) == 0 && 2 - (a2 <= 0) <= (char)sub_1411DCD00(a1, 0, 0) )
    return a1;
  return v6;
}
