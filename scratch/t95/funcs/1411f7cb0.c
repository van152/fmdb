// THUNK ALIAS -> sub_14402E280 (jmp:0x1411f7cb0->0x14402e280)
void __fastcall sub_14402E280(__int64 a1)
{
  int v2; // ebx
  __int64 v3; // rdi
  __int64 *v4; // rax
  volatile signed __int32 **v5; // r14
  __int64 v6; // rdx
  volatile signed __int32 *v7; // rax
  volatile signed __int32 *v8; // rcx
  volatile signed __int32 *v9; // rbx
  volatile signed __int32 *v10; // rbx
  __int64 v11; // r8
  __int64 v12; // rcx
  unsigned __int64 v13; // rcx
  unsigned __int64 i; // rdx
  int v15; // eax
  __int64 *v16; // rax
  volatile signed __int32 **v17; // r14
  __int64 v18; // rdx
  volatile signed __int32 *v19; // rax
  volatile signed __int32 *v20; // rcx
  volatile signed __int32 *v21; // rbx
  volatile signed __int32 *v22; // rbx

  if ( (_BYTE)word_141B60320 != 0 && *(_BYTE *)(a1 + 186) == 0 && *(_QWORD *)(a1 + 216) == 0 )
  {
    v2 = *(_DWORD *)(a1 + 12);
    if ( v2 != -1 )
    {
      v3 = sub_140F74650(qword_141B5FE40, (unsigned int)v2);
      if ( v3 != 0 )
      {
LABEL_7:
        if ( *(_QWORD *)(v3 + 48) != a1 )
        {
          v4 = (__int64 *)(*(__int64 (__fastcall **)(__int64))(*(_QWORD *)a1 + 368LL))(a1);
          v5 = (volatile signed __int32 **)(v3 + 24);
          if ( (__int64 *)(v3 + 24) != v4 )
          {
            v6 = *v4;
            v7 = *v5;
            v8 = *v5 - 1;
            if ( *v5 == nullptr )
              v8 = nullptr;
            v9 = (volatile signed __int32 *)(v6 - 4);
            if ( v6 != 0 )
            {
              if ( v7 != nullptr && _InterlockedDecrement(v8) == 0 )
                sub_1412EC9A0((__int64)v8);
              *v5 = nullptr;
              _InterlockedIncrement(v9);
              v10 = v9 + 1;
            }
            else
            {
              if ( v7 != nullptr && _InterlockedDecrement(v8) == 0 )
                sub_1412EC9A0((__int64)v8);
              v10 = nullptr;
            }
            *v5 = v10;
          }
          v16 = (__int64 *)(*(__int64 (__fastcall **)(__int64))(*(_QWORD *)a1 + 376LL))(a1);
          v17 = (volatile signed __int32 **)(v3 + 32);
          if ( (__int64 *)(v3 + 32) != v16 )
          {
            v18 = *v16;
            v19 = *v17;
            v20 = *v17 - 1;
            if ( *v17 == nullptr )
              v20 = nullptr;
            v21 = (volatile signed __int32 *)(v18 - 4);
            if ( v18 != 0 )
            {
              if ( v19 != nullptr && _InterlockedDecrement(v20) == 0 )
                sub_1412EC9A0((__int64)v20);
              *v17 = nullptr;
              _InterlockedIncrement(v21);
              v22 = v21 + 1;
            }
            else
            {
              if ( v19 != nullptr && _InterlockedDecrement(v20) == 0 )
                sub_1412EC9A0((__int64)v20);
              v22 = nullptr;
            }
            *v17 = v22;
          }
          *(_BYTE *)(v3 + 42) = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)a1 + 384LL))(a1);
          *(_BYTE *)(v3 + 43) = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)a1 + 392LL))(a1);
        }
      }
      else if ( v2 >= 0 && (_BYTE)word_141B60320 == 0 )
      {
        v11 = *(_QWORD *)(qword_141B5FE40 + 96);
        v12 = *(_QWORD *)(qword_141B5FE40 + 104) - v11;
        if ( v12 != 0 )
        {
          v13 = v12 >> 3;
          for ( i = 0; i < v13; ++i )
          {
            v3 = *(_QWORD *)(v11 + 8 * i);
            if ( v3 != 0 )
            {
              v15 = *(_DWORD *)(v3 + 12);
              if ( v15 == v2 )
                goto LABEL_7;
              if ( v15 > v2 )
                break;
            }
          }
        }
      }
    }
  }
}
