char __fastcall sub_143CA2E60(__int64 a1, char a2, unsigned int a3, __int64 a4)
{
  int v4; // r10d
  __int64 **v5; // rdi
  __int64 *v6; // rax
  __int64 *v7; // r11
  int v8; // esi
  __int64 v9; // rcx

  v4 = -1;
  if ( a2 == 20 )
    v4 = 22;
  v5 = *(__int64 ***)(qword_141B60198 + 128);
  v6 = *v5;
  v7 = v5[1];
  if ( *v5 == v7 )
    return 1;
  v8 = *(_DWORD *)(a1 + 12);
  while ( 1 )
  {
    v9 = *v6;
    if ( *(_DWORD *)(*v6 + 76) == v8 && (*(_BYTE *)(v9 + 94) == a2 || v4 == *(char *)(v9 + 94)) )
      break;
    if ( ++v6 == v7 )
      return 1;
  }
  return sub_1415446A0(v9, a3, a4);
}
