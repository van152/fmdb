char __fastcall sub_143F8B4B0(__int64 a1, __int64 a2, __int64 *a3, __int64 a4)
{
  __int64 v5; // rax
  __int64 v6; // rax
  __int64 v7; // rcx
  __int64 v8; // rdx
  __int64 v9; // r8
  __int64 v10; // r9
  __int64 *v11; // rdi
  __int64 v12; // rax
  __int64 v13; // rcx
  __int64 v14; // rax
  __int64 v15; // rcx
  __int64 v16; // rdx
  __int64 v17; // r8
  __int64 v18; // r9
  __int64 v19; // rax
  __int64 v20; // rcx
  __int64 v21; // rdx
  __int64 v22; // r8
  __int64 v23; // r9
  __int64 *v24; // rdi
  __int64 v25; // rax
  __int64 v26; // rcx
  __int64 v27; // rax
  __int64 v28; // rcx
  __int64 v29; // rdx
  __int64 v30; // r8
  __int64 v31; // r9
  __int64 v33; // [rsp+28h] [rbp-18h] BYREF
  _QWORD v34[4]; // [rsp+30h] [rbp-10h] BYREF

  v34[1] = -2;
  if ( (int)a2 > 1348890208 )
  {
    if ( (_DWORD)a2 == 1349742177 )
    {
      v24 = (__int64 *)(a1 + 40);
      v25 = sub_14083D4F0(a1, a2, a3, a4);
      v34[0] = 0;
      if ( v34 != v24 )
      {
        v26 = *v24;
        if ( *v24 != 0 )
          _InterlockedIncrement((volatile signed __int32 *)(v26 - 4));
        v34[0] = v26;
      }
      v5 = v25 + 136;
      v33 = v5;
      if ( &v33 != a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
        v27 = v33;
        v28 = v34[0];
        a3[1] = v34[0];
        *a3 = v27;
        v5 = sub_14083D4F0(a1: v28, a2: v29, a3: v30, a4: v31) + 8;
        v34[0] = 0;
        v33 = v5;
      }
      goto LABEL_25;
    }
    if ( (_DWORD)a2 == 1348890209 )
    {
      v11 = (__int64 *)(a1 + 32);
      v12 = sub_14083D4F0(a1, a2, a3, a4);
      v34[0] = 0;
      if ( v34 != v11 )
      {
        v13 = *v11;
        if ( *v11 != 0 )
          _InterlockedIncrement((volatile signed __int32 *)(v13 - 4));
        v34[0] = v13;
      }
      v5 = v12 + 136;
      v33 = v5;
      if ( &v33 != a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
        v14 = v33;
        v15 = v34[0];
        a3[1] = v34[0];
        *a3 = v14;
        v5 = sub_14083D4F0(a1: v15, a2: v16, a3: v17, a4: v18) + 8;
        v34[0] = 0;
        v33 = v5;
      }
      goto LABEL_25;
    }
  }
  else
  {
    if ( (_DWORD)a2 == 1145392197 )
    {
      v5 = sub_14083D4F0(a1, a2, a3, a4) + 24;
      LOBYTE(v34[0]) = 0;
      v33 = v5;
      if ( &v33 != a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
        v19 = v33;
        v20 = v34[0];
        a3[1] = v34[0];
        *a3 = v19;
        v5 = sub_14083D4F0(a1: v20, a2: v21, a3: v22, a4: v23) + 8;
        v34[0] = 0;
        v33 = v5;
      }
      goto LABEL_25;
    }
    if ( (_DWORD)a2 == 1313096770 )
    {
      v5 = sub_14083D4F0(a1, a2, a3, a4) + 24;
      LOBYTE(v34[0]) = 0;
      v33 = v5;
      if ( &v33 != a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
        v6 = v33;
        v7 = v34[0];
        a3[1] = v34[0];
        *a3 = v6;
        v5 = sub_14083D4F0(a1: v7, a2: v8, a3: v9, a4: v10) + 8;
        v34[0] = 0;
        v33 = v5;
      }
LABEL_25:
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v5 + 16LL))(a1: v5, a2: &v33);
      return 1;
    }
  }
  return sub_14109AD50(a1, a2, a3);
}
