__int64 __fastcall sub_143D25100(__int64 a1, int a2)
{
  volatile signed __int32 **v4; // r14
  __int64 v5; // r8
  volatile signed __int32 *v6; // rdi
  __int64 v7; // rbx
  volatile signed __int32 *v8; // rbp
  __int64 v9; // r8
  int v10; // ebp
  __int64 *v11; // rax
  __int64 *v12; // rcx
  __int64 *v13; // rdx
  __int64 *v14; // rdi
  __int64 v15; // rcx
  volatile signed __int32 *v16; // rcx
  volatile signed __int32 *v17; // rcx
  __int64 v18; // rcx
  volatile signed __int32 *v20; // [rsp+40h] [rbp-58h] BYREF
  int v21; // [rsp+4Ch] [rbp-4Ch] BYREF
  unsigned int v22; // [rsp+50h] [rbp-48h] BYREF
  volatile signed __int32 *v23; // [rsp+58h] [rbp-40h] BYREF
  _QWORD v24[7]; // [rsp+60h] [rbp-38h] BYREF

  v24[0] = 0;
  sub_14080D0E0(a1: &v22, a2: 0x1418E2C24LL);
  LODWORD(v4) = 0;
  LOBYTE(v5) = 1;
  sub_140FFADB0(a1, a2: v24, a3: v5, a4: 0);
  sub_1407D0F70(
    a1: (unsigned int)&v20,
    a2: (unsigned int)&v23,
    a3: a2,
    a4: (unsigned int)v24,
    a5: (__int64)&v22,
    a6: 0,
    a7: 0,
    0,
    0x80100004E554C4CLL);
  if ( v23 == nullptr )
    goto LABEL_30;
  v20 = v23;
  _InterlockedIncrement(v23 + 2);
  v6 = v20;
  (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *, __int64))(*(_QWORD *)v20 + 40LL))(
    a1: v20,
    a2: &v22,
    a3: 4);
  if ( *((_DWORD *)v6 + 4) != 0 )
  {
LABEL_3:
    LODWORD(v4) = 0;
    goto LABEL_24;
  }
  if ( v22 != 0 )
  {
    v7 = 0;
    v4 = &v20;
    while ( 1 )
    {
      v21 = v7;
      v8 = v20;
      (*(void (__fastcall **)(volatile signed __int32 *, int *, __int64))(*(_QWORD *)v20 + 40LL))(
        a1: v20,
        a2: &v21,
        a3: 4);
      if ( *((_DWORD *)v8 + 4) != 0 )
        goto LABEL_3;
      v10 = v21;
      if ( *(_QWORD *)(a1 + 40) == 0
        && (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)a1 + 48LL))(a1) > (unsigned __int64)v10 )
      {
        goto LABEL_19;
      }
      v11 = *(__int64 **)(a1 + 32);
      v12 = (__int64 *)v11[1];
      v13 = v11;
      if ( *((_BYTE *)v12 + 25) == 0 )
      {
        v13 = *(__int64 **)(a1 + 32);
        do
        {
          v14 = v12 + 2;
          if ( *((_DWORD *)v12 + 7) >= v10 )
          {
            v13 = v12;
            v14 = v12;
          }
          v12 = (__int64 *)*v14;
        }
        while ( *(_BYTE *)(*v14 + 25) == 0 );
      }
      if ( *((_BYTE *)v13 + 25) == 0 && *((_DWORD *)v13 + 7) <= v10 )
        break;
LABEL_15:
      v15 = 0;
LABEL_21:
      LOBYTE(v9) = 1;
      if ( (unsigned __int8)sub_1411A1F80(a1: v15, a2: &v20, a3: v9) == 0 )
        goto LABEL_3;
      if ( ++v7 >= (unsigned __int64)v22 )
        goto LABEL_23;
    }
    v15 = 0;
    if ( v13 == v11 )
      goto LABEL_21;
    v10 = *((_DWORD *)v13 + 8);
LABEL_19:
    if ( v10 >= 0 )
    {
      v15 = *(_QWORD *)(**(_QWORD **)(a1 + 128) + 8LL * (unsigned int)v10);
      goto LABEL_21;
    }
    goto LABEL_15;
  }
LABEL_23:
  *(_BYTE *)(a1 + 91) = 0;
  LOBYTE(v4) = 1;
LABEL_24:
  v16 = v20;
  if ( v20 != nullptr && _InterlockedDecrement(v20 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v16)(a1: v16, a2: 1);
  v17 = v23;
  if ( v23 != nullptr && _InterlockedDecrement(v23 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v17)(a1: v17, a2: 1);
LABEL_30:
  v18 = v24[0];
  if ( v24[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v24[0] - 4LL)) == 0 )
    sub_1412EC9A0(a1: v18 - 4);
  return (unsigned int)v4;
}
