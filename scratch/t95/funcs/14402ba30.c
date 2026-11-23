bool __fastcall sub_14402BA30(__int64 a1)
{
  _QWORD *v1; // rax
  _QWORD *v2; // rsi
  __int64 v3; // rax
  __int64 v4; // rcx
  __int64 v5; // rax

  v1 = *(_QWORD **)(a1 + 24);
  if ( v1 == *(_QWORD **)(a1 + 32) )
    return false;
  v2 = (_QWORD *)*v1;
  if ( *v1 == 0 || (unsigned __int8)sub_140087070() == 0 )
    return false;
  v3 = v2[10];
  if ( v2[6] == 0 || v3 == 0 || *(_DWORD *)(v3 + 12) != 129985 )
  {
    if ( v2[11] != 0 )
      v3 = v2[11];
    if ( v3 == 0 || *(_DWORD *)(v3 + 12) != 129985 )
      return false;
  }
  v4 = *(_QWORD *)(v3 + 96);
  if ( *(_BYTE *)(v3 + 245) == 0 || (v5 = *(_QWORD *)(v4 + 272)) == 0 )
    v5 = *(_QWORD *)(v4 + 264);
  return *(_BYTE *)(v5 + 1150) >= 0;
}
