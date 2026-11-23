bool __fastcall sub_14438C670(_QWORD *a1, _QWORD *a2)
{
  _DWORD *v4; // rcx
  __int64 v5; // rdi
  unsigned __int64 v6; // rbp
  __int64 v7; // r15
  _WORD *v8; // rbx
  _DWORD *v9; // rbx
  __int64 v10; // rbx
  unsigned __int8 v12; // [rsp+27h] [rbp-51h] BYREF
  _BYTE v13[4]; // [rsp+28h] [rbp-50h] BYREF
  unsigned int v14; // [rsp+2Ch] [rbp-4Ch] BYREF
  char v15; // [rsp+33h] [rbp-45h] BYREF
  _WORD v16[34]; // [rsp+34h] [rbp-44h] BYREF

  if ( *a1 != a1[1] )
    a1[1] = *a1;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v14, a3: 4);
  sub_14145CF20(a1, a2: v14, a3: v13);
  v4 = (_DWORD *)*a2;
  if ( v14 == 0 )
    return v4[4] == 0;
  v5 = 0;
  v6 = 0;
  while ( 1 )
  {
    v7 = *a1;
    v8 = (_WORD *)(*a1 + v5);
    (*(void (__fastcall **)(_DWORD *, unsigned __int8 *, __int64))(*(_QWORD *)v4 + 40LL))(a1: v4, a2: &v12, a3: 1);
    (*(void (__fastcall **)(_QWORD, _WORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v8, a3: 2);
    if ( v12 <= 2u && (*v8 & 0x1FC0) == 0x380 )
      *v8 = *v8 & 0xE03F | 0x3C0;
    v9 = (_DWORD *)*a2;
    if ( *(_DWORD *)(*a2 + 16LL) != 0 )
      break;
    (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)v9 + 40LL))(a1: *a2, a2: &v15, a3: 1);
    if ( v9[4] != 0 )
      break;
    v10 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v7 + v5 + 2, a3: 11);
    if ( *(_DWORD *)(v10 + 16) != 0 )
      break;
    if ( *(_DWORD *)(*a2 + 16LL) != 0 )
      break;
    (*(void (__fastcall **)(_QWORD, _WORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v16, a3: 4);
    *(_WORD *)(v7 + v5 + 14) = v16[0];
    v4 = (_DWORD *)*a2;
    if ( *(_DWORD *)(*a2 + 16LL) != 0 )
      break;
    ++v6;
    v5 += 16;
    if ( v6 >= v14 )
      return true;
  }
  return false;
}
