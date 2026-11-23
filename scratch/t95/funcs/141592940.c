char __fastcall sub_141592940(__int64 a1, int a2, __int64 *a3)
{
  __int64 v5; // rbx
  volatile signed __int32 *v6; // rdx
  unsigned int v7; // esi
  __int64 *v8; // rcx
  __int64 v9; // rax
  __int64 v10; // rcx
  unsigned __int64 v11; // rcx
  bool v12; // di
  unsigned __int64 v13; // rsi
  __int64 v14; // rbx
  __int64 *v15; // rbx
  __int64 v17; // rcx
  __int64 *v18; // rcx
  __int64 v19; // rax
  __int64 v20; // rcx
  unsigned __int64 v21; // rcx
  bool v22; // bl
  unsigned __int64 v23; // rsi
  __int64 v24; // rdi
  __int64 *v25; // rdi
  __int64 v26; // rdx
  unsigned int v27; // edi
  volatile signed __int32 *v28; // rbx
  __int64 v29; // rsi
  __int64 v30; // r14
  __int64 v31; // rcx
  __int64 v32; // rax
  char v33; // si
  __int64 v34; // rax
  __int64 v35; // rax
  __int64 v36; // rcx
  volatile signed __int32 *v37; // rcx
  __int64 v38; // [rsp+20h] [rbp-30h] BYREF
  __int64 v39; // [rsp+28h] [rbp-28h]
  volatile signed __int32 *v40[2]; // [rsp+30h] [rbp-20h] BYREF
  __int64 v41; // [rsp+48h] [rbp-8h]

  v41 = -2;
  if ( a2 != 1347710561 )
    return sub_140FE3F20((_DWORD *)a1, a2, a3);
  *(_OWORD *)v40 = 0;
  v5 = sub_1412EC810(264, 1024);
  *(_QWORD *)v5 = 0x40000000000LL;
  *(_BYTE *)(v5 + 8) = 0;
  v6 = v40[0];
  if ( v40[0] == nullptr )
    goto LABEL_11;
  v7 = 1024;
  if ( SHIDWORD(v40[1]) < 1024 )
    v7 = HIDWORD(v40[1]);
  if ( SHIDWORD(v40[1]) > 0 )
  {
    sub_141758A00(v5 + 8, v40[0] + 2, v7);
    *(_BYTE *)(v5 + 8 + v7) = 0;
    v6 = v40[0];
  }
  HIDWORD(v40[1]) = v7;
  if ( v6 != (volatile signed __int32 *)v5 )
  {
    if ( v6 != nullptr && _InterlockedDecrement(v6) == 0 )
      sub_1412EC9A0(v6, v6);
LABEL_11:
    LODWORD(v40[1]) = 0;
    _InterlockedIncrement((volatile signed __int32 *)v5);
    v40[0] = (volatile signed __int32 *)v5;
    LODWORD(v40[1]) = *(_DWORD *)(v5 + 4);
  }
  v8 = *(__int64 **)(a1 + 24);
  if ( v8 != nullptr && (v9 = *v8, (v10 = v8[1] - *v8) != 0) )
  {
    v11 = v10 >> 3;
    v12 = true;
    v13 = 1;
    while ( 1 )
    {
      v15 = *(__int64 **)(v9 + 8 * v13 - 8);
      if ( *((_WORD *)v15 + 4) == 3 && *((_BYTE *)v15 + 10) == 0xFF )
        break;
      v12 = v13 < v11;
      v14 = v13 - v11 + 1;
      ++v13;
      if ( v14 == 1 )
      {
        v15 = &qword_141B59EE0;
        break;
      }
    }
    sub_140806590(v40, 1024);
    sub_140806120(v40, v15);
    if ( v12 )
    {
LABEL_33:
      if ( v40[0] == nullptr )
        goto LABEL_38;
      v27 = HIDWORD(v40[1]);
      v28 = v40[0] + 2;
      if ( HIDWORD(v40[1]) == -1 )
        v27 = sub_141758DB0(v40[0] + 2);
      if ( (int)v27 > 0 )
      {
        v29 = sub_1412EC810(264, v27);
        *(_DWORD *)v29 = 0;
        v30 = v29 + 4;
        *(_DWORD *)(v29 + 4) = v27;
        sub_141758A00(v29 + 8, v28, v27);
        *(_BYTE *)(v29 + v27 + 8) = 0;
        _InterlockedIncrement((volatile signed __int32 *)v29);
        v32 = sub_14083D4F0(v31);
        v39 = 0;
        _InterlockedIncrement((volatile signed __int32 *)v29);
        v33 = 0;
      }
      else
      {
LABEL_38:
        v33 = 1;
        v30 = 0;
        v32 = sub_14083D4F0(v17);
      }
      v39 = v30;
      v34 = v32 + 136;
      v38 = v34;
      if ( &v38 != a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v35 = v38;
        v36 = v39;
        a3[1] = v39;
        *a3 = v35;
        v34 = sub_14083D4F0(v36) + 8;
        v39 = 0;
        v38 = v34;
      }
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v34 + 16LL))(v34, &v38);
      if ( v33 == 0 && _InterlockedDecrement((volatile signed __int32 *)(v30 - 4)) == 0 )
        sub_1412EC9A0(v30 - 4, v26);
      goto LABEL_44;
    }
  }
  else
  {
    sub_140806590(v40, 1024);
    sub_140806120(v40, &qword_141B59EE0);
  }
  v18 = *(__int64 **)(a1 + 24);
  if ( v18 != nullptr )
  {
    v19 = *v18;
    v20 = v18[1] - *v18;
    if ( v20 != 0 )
    {
      v21 = v20 >> 3;
      v22 = true;
      v23 = 1;
      while ( 1 )
      {
        v25 = *(__int64 **)(v19 + 8 * v23 - 8);
        if ( *((_WORD *)v25 + 4) == 3 && *((_BYTE *)v25 + 10) == 0 )
          break;
        v22 = v23 < v21;
        v24 = v23 - v21 + 1;
        ++v23;
        if ( v24 == 1 )
        {
          v25 = &qword_141B59EE0;
          break;
        }
      }
      sub_140806590(v40, 1024);
      sub_140806120(v40, v25);
      if ( !v22 )
        goto LABEL_44;
      goto LABEL_33;
    }
  }
  sub_140806590(v40, 1024);
  sub_140806120(v40, &qword_141B59EE0);
LABEL_44:
  v37 = v40[0];
  if ( v40[0] != nullptr && _InterlockedDecrement(v40[0]) == 0 )
    sub_1412EC9A0(v37, v26);
  return 1;
}
