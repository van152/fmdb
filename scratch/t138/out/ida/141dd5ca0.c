__int64 __fastcall sub_141DD5CA0(__int64 a1, int a2)
{
  volatile signed __int32 *v3; // rsi
  unsigned __int64 v4; // rsi
  __int64 v5; // rdi
  volatile signed __int32 *v6; // rbx
  __int64 v7; // rax
  __int64 v8; // rdx
  __int64 v9; // rbx
  __int64 v10; // rax
  __int64 v11; // rdi
  unsigned __int64 v12; // rdi
  __int64 v13; // rax
  volatile signed __int32 *v14; // rcx
  char v16; // [rsp+47h] [rbp-81h] BYREF
  volatile signed __int32 *v17; // [rsp+48h] [rbp-80h] BYREF
  int v18; // [rsp+50h] [rbp-78h] BYREF
  int v19; // [rsp+54h] [rbp-74h] BYREF
  _DWORD v20[6]; // [rsp+58h] [rbp-70h] BYREF
  _BYTE v21[24]; // [rsp+70h] [rbp-58h] BYREF
  _BYTE v22[64]; // [rsp+88h] [rbp-40h] BYREF

  sub_1407D0D60(a1: v22);
  sub_1407D0F70(
    a1: (unsigned int)v22,
    a2: (unsigned int)&v17,
    a3: a2,
    a4: (unsigned int)&unk_141ABEA78,
    a5: (__int64)&unk_141B59880,
    a6: 0,
    a7: 0,
    0);
  v3 = v17;
  if ( v17 == nullptr )
  {
    LODWORD(v4) = 0;
    return (unsigned int)v4;
  }
  (*(void (__fastcall **)(volatile signed __int32 *, int *, __int64))(*(_QWORD *)v17 + 40LL))(a1: v17, a2: &v19, a3: 4);
  if ( *((_DWORD *)v3 + 4) == 0 )
  {
    LODWORD(v4) = v19;
    if ( (_DWORD)v4 == (unsigned int)sub_140F601E0() )
    {
      if ( sub_140F617F0() == 0 )
      {
LABEL_17:
        if ( sub_140F459E0() != 0 )
        {
          v4 = 0;
          do
            *(_QWORD *)(sub_140F45D40(a1: (unsigned int)v4++) + 176) = 0;
          while ( v4 < sub_140F459E0() );
        }
        LOBYTE(v4) = 1;
        if ( sub_140F5A9A0() != 0 )
        {
          v12 = 0;
          do
          {
            v13 = sub_140F5C7E0(a1: (unsigned int)v12);
            sub_1411A7600(a1: v13);
            ++v12;
          }
          while ( v12 < sub_140F5A9A0() );
        }
        goto LABEL_27;
      }
      v4 = 0;
      while ( 1 )
      {
        v5 = sub_140F61810(a1: (unsigned int)v4);
        v6 = v17;
        (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v17 + 40LL))(
          a1: v17,
          a2: &v16,
          a3: 1);
        if ( *((_DWORD *)v6 + 4) != 0 )
          break;
        *(_BYTE *)(v5 + 458) = v16;
        v7 = sub_1410403F0(a1: v5, a2: 0);
        if ( v7 != 0 )
        {
          v9 = v7;
          sub_1407C9510(a1: v21);
          sub_140839290(a1: v17, a2: v20, a3: v21);
          if ( v20[0] != 0 )
            goto LABEL_25;
          sub_141063C00(a1: v9, a2: v21);
          sub_1407C9510(a1: v20);
          sub_140839480(a1: v17, a2: &v18, a3: v20);
          if ( v18 != 0 )
            goto LABEL_24;
          sub_14083C130(a1: v9 + 1184, a2: v20);
          sub_14083ADA0(a1: v20);
          sub_140833970(a1: v21);
        }
        LOBYTE(v8) = 1;
        v10 = sub_1410403F0(a1: v5, a2: v8);
        if ( v10 != 0 )
        {
          v11 = v10;
          sub_1407C9510(a1: v21);
          sub_140839290(a1: v17, a2: v20, a3: v21);
          if ( v20[0] != 0 )
            goto LABEL_25;
          sub_141063C00(a1: v11, a2: v21);
          sub_1407C9510(a1: v20);
          sub_140839480(a1: v17, a2: &v18, a3: v20);
          if ( v18 != 0 )
          {
LABEL_24:
            sub_14083ADA0(a1: v20);
LABEL_25:
            sub_140833970(a1: v21);
            break;
          }
          sub_14083C130(a1: v11 + 1184, a2: v20);
          sub_14083ADA0(a1: v20);
          sub_140833970(a1: v21);
        }
        if ( ++v4 >= sub_140F617F0() )
          goto LABEL_17;
      }
    }
  }
  LODWORD(v4) = 0;
LABEL_27:
  v14 = v17;
  if ( v17 != nullptr && _InterlockedDecrement(v17 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v14)(a1: v14, a2: 1);
  return (unsigned int)v4;
}
