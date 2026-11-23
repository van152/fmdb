// THUNK ALIAS -> sub_14402AD30 (jmp:0x1411f0820->0x14402ad30)
bool __fastcall sub_14402AD30(__int64 a1, char a2)
{
  _QWORD *v2; // rax
  _QWORD *v3; // rsi
  __int64 v5; // rax
  __int64 v6; // rcx
  __int64 v7; // rdx
  __int64 v8; // rcx

  v2 = *(_QWORD **)(a1 + 24);
  if ( v2 == *(_QWORD **)(a1 + 32) )
    return false;
  v3 = (_QWORD *)*v2;
  if ( *v2 == 0 || (unsigned __int8)sub_140087070() == 0 )
    return false;
  v5 = v3[10];
  if ( v3[6] == 0 || v5 == 0 || *(_DWORD *)(v5 + 12) != 40 )
  {
    if ( v3[11] != 0 )
      v5 = v3[11];
    if ( v5 == 0 || *(_DWORD *)(v5 + 12) != 40 )
      return false;
  }
  v6 = *(_QWORD *)(v5 + 96);
  if ( v6 == 0 )
    return false;
  if ( *(_BYTE *)(v5 + 245) == 0 || (v7 = *(_QWORD *)(v6 + 272)) == 0 )
    v7 = *(_QWORD *)(v6 + 264);
  return *(char *)(v7 + 1150) >= 0 && (a2 == 0 || (v8 = *(_QWORD *)(v5 + 176)) != 0 && sub_1409083C0(v8));
}
