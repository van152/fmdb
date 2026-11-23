char __fastcall sub_143EE8CC0(__int64 a1, __int64 a2, __int64 *a3)
{
  unsigned __int16 v4; // dx
  __int64 v5; // rcx
  char v6; // r14
  __int64 v7; // rax
  __int64 v8; // rax
  __int64 v9; // rcx
  __int64 v11; // rbx
  __int64 v12; // [rsp+28h] [rbp-18h] BYREF
  __int64 v13; // [rsp+30h] [rbp-10h]
  __int64 v14; // [rsp+38h] [rbp-8h]

  v14 = -2;
  if ( (int)a2 <= 1315332472 )
  {
    if ( (_DWORD)a2 != 1130917965 && (_DWORD)a2 != 1131245645 && (_DWORD)a2 != 1315006073 )
      return sub_1411B01B0(a1, a2, a3);
  }
  else if ( (_DWORD)a2 != 1315332473 && (_DWORD)a2 != 1315333241 )
  {
    if ( (_DWORD)a2 != 1416586854 )
      return sub_1411B01B0(a1, a2, a3);
    v4 = *(_WORD *)(a1 + 222);
    v5 = *(_WORD *)(a1 + 220) & 0x1FF;
    v6 = 1;
    if ( ((_WORD)v5 != 1 || v4 != 1900)
      && v4 <= HIWORD(dword_141AAE084)
      && (v4 < HIWORD(dword_141AAE084) || (unsigned __int16)(dword_141AAE084 & 0x1FF) >= (unsigned __int16)v5) )
    {
      v6 = 0;
    }
    v7 = sub_14083D4F0(v5) + 24;
    LOBYTE(v13) = v6;
    v12 = v7;
    if ( &v12 != a3 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      v8 = v12;
      v9 = v13;
      a3[1] = v13;
      *a3 = v8;
      v7 = sub_14083D4F0(v9) + 8;
      v13 = 0;
      v12 = v7;
    }
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v7 + 16LL))(v7, &v12);
    return 1;
  }
  v11 = 368;
  if ( *(_BYTE *)(a1 + 47) == 0 )
    v11 = 216;
  return sub_141042940(*(_QWORD *)(*(_QWORD *)(a1 + 48) + v11), a2, a3, 1);
}
