// THUNK ALIAS -> sub_143BDD7C0 (jmp:0x140e35350->0x143bdd7c0)
__int64 __fastcall sub_143BDD7C0(_QWORD *a1, _QWORD *a2)
{
  __int64 v2; // rax
  _QWORD *v3; // rdi
  __int64 v6; // rax
  __int64 v7; // rdx
  __int64 v8; // rcx
  __int64 v9; // rax
  __int64 v10; // rax
  __int16 v11; // dx
  __int16 v12; // cx
  __int64 v13; // rbp
  __int64 v14; // rbp
  unsigned int v15; // r12d
  unsigned int v16; // r14d
  __int64 v17; // r15
  _QWORD *v19; // rbx
  __int64 v20; // r13
  unsigned __int8 v21; // al
  __int64 v22; // rsi
  __int64 v24; // rax
  unsigned __int16 v25; // cx
  unsigned __int16 v26; // [rsp+28h] [rbp-50h]
  unsigned __int16 v27; // [rsp+2Ch] [rbp-4Ch]
  _QWORD *v28; // [rsp+30h] [rbp-48h]

  v2 = a1[31];
  if ( v2 == 0 )
    return 0;
  v3 = *(_QWORD **)(v2 + 88);
  if ( v3 == nullptr )
    return 0;
  v6 = sub_140DE2490((char *)a1 + *(int *)(a1[1] + 8LL) + 344);
  if ( v6 != 0 || (v6 = a1[38]) != 0 )
  {
    v26 = 1900;
    LOWORD(v7) = 1;
    if ( *(_BYTE *)(v6 + 47) == 0 )
    {
      v8 = *(_QWORD *)(v6 + 48);
      if ( v8 != 0 )
      {
        LOBYTE(v7) = 1;
        v9 = (*(__int64 (__fastcall **)(__int64, __int64))(*(_QWORD *)v8 + 440LL))(v8, v7);
        if ( v9 != 0 && (v10 = *(_QWORD *)(v9 + 440)) != 0 )
        {
          v11 = *(_WORD *)(v10 + 6);
          v26 = HIWORD(dword_141AAE084);
        }
        else
        {
          v12 = 3;
          if ( (unsigned __int16)(23593 * HIWORD(dword_141AAE084)) < 0xA3Eu )
            v12 = 15;
          v26 = HIWORD(dword_141AAE084);
          v11 = ((unsigned __int16)(HIWORD(dword_141AAE084) & v12) == 0) + 171;
        }
        if ( v11 >= (__int16)((dword_141AAE084 & 0x1FF) - 1) )
          --v26;
        LOWORD(v7) = (v11 + 1) & 0x1FF;
      }
    }
  }
  else
  {
    v26 = 1900;
    LOWORD(v7) = 1;
  }
  v13 = v3[1] - *v3;
  if ( v13 == 0 )
    return 0;
  v27 = v7;
  v28 = a2;
  v14 = v13 >> 3;
  LOWORD(v15) = 1;
  LOWORD(v16) = 1900;
  v17 = 0;
  do
  {
    v19 = *(_QWORD **)(*v3 + 8 * v14-- - 8);
    v20 = v19[1];
    if ( *(_BYTE *)(v20 + 47) != 1 )
    {
      v21 = (*(__int64 (__fastcall **)(_QWORD *))(*v19 + 40LL))(v19);
      if ( v21 != 0 )
      {
        v22 = v21 - 1LL;
        while ( 1 )
        {
          v24 = (*(__int64 (__fastcall **)(_QWORD *, __int64))(*v19 + 56LL))(v19, v22);
          if ( v24 != 0 && *(_QWORD *)(v24 + 8) != 0 )
            break;
          if ( v22-- == 0 )
            goto LABEL_22;
        }
        v25 = *(_WORD *)(v24 + 18);
        if ( (v26 < v25 || v26 <= v25 && v27 < (unsigned __int16)(*(_WORD *)(v24 + 16) & 0x1FF))
          && (v17 == 0
           || (unsigned __int16)v16 < v25
           || (unsigned __int16)v16 <= v25
           && (unsigned __int16)(v15 & 0x1FF) < (unsigned __int16)(*(_WORD *)(v24 + 16) & 0x1FF)) )
        {
          v15 = *(_DWORD *)(v24 + 16);
          v16 = HIWORD(v15);
          *v28 = v20;
          v17 = v24;
        }
      }
    }
LABEL_22:
    ;
  }
  while ( v14 != 0 );
  return v17;
}
