// THUNK ALIAS -> sub_143CA3C40 (jmp:0x140ecdae0->0x143ca3c40)
__int64 __fastcall sub_143CA3C40(__int64 a1)
{
  __int64 v2; // rcx
  int v3; // eax
  int v4; // ecx
  __int64 v5; // rdi
  __int64 v6; // rdi
  __int64 v7; // r15
  __int64 *v8; // rdx
  __int64 v9; // rcx
  __int64 v10; // rdx
  __int64 v11; // rbx
  __int64 v12; // rax
  __int64 v13; // rax
  __int64 v14; // rcx
  __int64 v15; // rbx
  __int64 v16; // rbx
  __int64 v17; // rax
  __int64 v18; // rcx
  __int64 v19; // rax
  __int64 v20; // rcx
  __int64 v21; // rax
  __int64 v22; // rax
  __int64 v23; // rcx
  __int64 v24; // rax
  __int64 *v25; // rbx
  unsigned __int64 v27; // [rsp+68h] [rbp-18h] BYREF
  __int64 v28; // [rsp+70h] [rbp-10h]
  __int64 v29[2]; // [rsp+80h] [rbp+0h] BYREF
  __int64 v30; // [rsp+90h] [rbp+10h] BYREF
  __int64 v31; // [rsp+98h] [rbp+18h]
  __int64 v32; // [rsp+A0h] [rbp+20h]

  v32 = -2;
  v29[1] = 0;
  v29[0] = sub_14083D4F0(a1) + 8;
  v2 = *(_QWORD *)(a1 + 96);
  if ( v2 != 0 )
  {
    v3 = *(_DWORD *)(v2 + 12);
    v4 = *(_DWORD *)(v2 + 16);
    if ( v4 == 0 )
      v4 = v3;
  }
  else
  {
    v3 = -1;
    v4 = -1;
  }
  v27 = __PAIR64__(v4, v3);
  sub_140FE72B0((int *)&v27, 1315856756, v29);
  v5 = *(_QWORD *)(*(_QWORD *)(qword_141B5FE40 + 128) + 8LL) - **(_QWORD **)(qword_141B5FE40 + 128);
  if ( v5 != 0 )
  {
    v6 = v5 >> 3;
    v7 = 0;
    do
    {
      if ( (int)v7 >= 0 )
      {
        if ( (_BYTE)word_141B60320 != 0 )
        {
          v8 = *(__int64 **)(qword_141B5FE40 + 128);
          v9 = *v8;
          v10 = v8[1];
        }
        else
        {
          v9 = *(_QWORD *)(qword_141B5FE40 + 96);
          v10 = *(_QWORD *)(qword_141B5FE40 + 104);
        }
        if ( (v10 - v9) >> 3 > (unsigned __int64)(unsigned int)v7 )
        {
          v11 = *(_QWORD *)(v9 + 8LL * (unsigned int)v7);
          if ( v11 != 0 )
          {
            v12 = *(_QWORD *)(v11 + 48);
            if ( v12 != 0 && *(_QWORD *)(v11 + 80) == a1 && **(_QWORD **)(v12 + 24) == v11 )
            {
              sub_1407C9510(&v27);
              v13 = *(int *)(v11 + 12);
              v14 = *(unsigned int *)(v11 + 16);
              v15 = *(unsigned int *)(v11 + 12);
              if ( (_DWORD)v14 != 0 )
                v15 = (unsigned int)v14;
              v16 = v13 | (v15 << 32);
              v17 = sub_14083D4F0(v14);
              v31 = v16;
              v30 = v17 + 72;
              sub_140835380((__int64 *)&v27, 1685417577, &v30);
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v30 + 16LL))(v30, &v30);
              v19 = sub_14083D4F0(v18);
              LODWORD(v31) = 3;
              v30 = v19 + 40;
              sub_140835380((__int64 *)&v27, 1685353593, &v30);
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v30 + 16LL))(v30, &v30);
              v21 = sub_14083D4F0(v20);
              LODWORD(v31) = 1131312233;
              v30 = v21 + 56;
              sub_140835380((__int64 *)&v27, 1886549113, &v30);
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v30 + 16LL))(v30, &v30);
              v22 = v27;
              v23 = v28;
              if ( v27 == v28 )
                goto LABEL_23;
              while ( *(_DWORD *)v22 != 1853322860 )
              {
                v22 += 16;
                if ( v22 == v28 )
                  goto LABEL_23;
              }
              if ( v22 == v28 || (v25 = *(__int64 **)(v22 + 8)) == nullptr )
              {
LABEL_23:
                sub_140835A40(&v27, 1853322860, v29);
              }
              else if ( v25 != v29 )
              {
                (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v25 + 16LL))(*v25, v25);
                (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)v29[0] + 24LL))(v29[0], v29, v25);
              }
              v24 = sub_14083D4F0(v23);
              LOBYTE(v31) = 1;
              v30 = v24 + 24;
              sub_140835380((__int64 *)&v27, 1230193478, &v30);
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v30 + 16LL))(v30, &v30);
              sub_140F47AD0((__int64)&qword_141B5FDA8, (__int64 *)&v27, 0, 1, 1, 1u, 1, nullptr, nullptr, 1, 0, 0);
              sub_140833970(&v27);
            }
          }
        }
      }
      ++v7;
    }
    while ( v7 != v6 );
  }
  return (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v29[0] + 16LL))(v29[0], v29);
}
