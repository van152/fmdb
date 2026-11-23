// THUNK ALIAS -> sub_14438B300 (jmp:0x14145bf70->0x14438b300)
bool __fastcall sub_14438B300(__int64 **a1, _QWORD *a2)
{
  __int64 *v3; // rax
  __int64 v4; // r15
  __int64 *v5; // rax
  __int64 v6; // rdi
  __int64 v7; // r13
  _QWORD *v8; // rsi
  __int64 v9; // rdi
  __int64 v10; // rdi
  __int64 v11; // rbp
  __int64 *v12; // rdx
  int v13; // eax
  __int64 v14; // rbx
  __int64 v16; // [rsp+20h] [rbp-58h]
  __int64 v17; // [rsp+28h] [rbp-50h] BYREF
  char v18; // [rsp+30h] [rbp-48h]

  v3 = *(__int64 **)(qword_141B5FDF8 + 128);
  v4 = v3[1];
  v16 = *v3;
  if ( v4 != *v3 )
  {
    v5 = *a1;
    v17 = 0;
    v18 = 100;
    v6 = *v5;
    sub_1408C9770(*v5 + 48, &v17);
    v7 = *(_QWORD *)(v6 + 56);
    v8 = (_QWORD *)(*(__int64 (__fastcall **)(_QWORD, _QWORD *, _QWORD))(*(_QWORD *)*a2 + 176LL))(*a2, a2, 0);
    v9 = v8[1] - *v8;
    if ( v9 != 0 )
    {
      v10 = v9 >> 4;
      v11 = 8;
      do
      {
        v12 = *(__int64 **)(*v8 + v11);
        if ( v12 == nullptr )
          v12 = &qword_141B5A4A0;
        v13 = *(_DWORD *)(*v8 + v11 - 8);
        if ( v13 == 1282172784 )
        {
          *(_BYTE *)(v7 - 8) = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v12 + 64LL))(*v12);
        }
        else if ( v13 == 1282172780 )
        {
          v14 = qword_141B5FDF8;
          sub_140FE7960((__int64)&v17, v12, 0x6C616E67u);
          *(_QWORD *)(v7 - 16) = sub_140FA1860(v14, (int *)&v17);
        }
        v11 += 16;
        --v10;
      }
      while ( v10 != 0 );
    }
  }
  return v4 != v16;
}
